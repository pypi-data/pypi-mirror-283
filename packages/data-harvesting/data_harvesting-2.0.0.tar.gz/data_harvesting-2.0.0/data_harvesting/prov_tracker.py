# -*- coding: utf-8 -*-
"""Implementation of a generic decorator that enables simple provenance tracking.

To see how to implement it for a specific data type, check out the example IntTracker.
"""
from __future__ import annotations

from uuid import UUID, uuid4
from copy import deepcopy
from typing import Union, Type, TypeVar, Generic, Optional, Tuple, List
import functools
import itertools
import wrapt
from datetime import datetime
import inspect
from pydantic import BaseModel, Field, PrivateAttr
from pathlib import Path


UnhideBaseModel = BaseModel  # NOTE: you would import Unhide BaseModel


class BaseProvMeta(UnhideBaseModel):
    """Generic provenance metadata about a performed computation."""

    # NOTE: extend/subclass this as needed for more kinds of information
    # NOTE: might want to auto-exclude defaults / None values for export

    timestamp: datetime = Field(default_factory=lambda: datetime.now())
    function_file: Optional[Path] = None
    function_file_line: Optional[int] = None
    function_module: Optional[str] = None
    function_name: Optional[str] = None

    @classmethod
    def from_object(cls, obj):
        """Return metadata about some object (e.g. a function or class)."""
        func_module = inspect.getmodule(obj)
        try:
            func_module_file = inspect.getfile(func_module)
        except TypeError:
            func_module_file = None

        return cls(
            function_name=obj.__qualname__,
            function_module=func_module.__name__,
            function_file=Path(func_module_file) if func_module_file else None,
        )

    @classmethod
    def from_here(cls):
        """Return metadata for the currently executed function."""
        code = inspect.currentframe().f_back.f_code
        return cls(
            function_file=code.co_filename,
            function_file_line=code.co_firstlineno,
            function_name=code.co_name,
        )


State = TypeVar('State')
Patch = TypeVar('Patch')


class BaseProvTracker(UnhideBaseModel, Generic[State, Patch]):
    """Class to manage state for linear tracking of data provenance.

    Works for types for which we can compute a diff and apply function
    (a `diff` and `apply` function must be implemented in a subclass).
    A patch may have a different type than the state (but may be the same).
    """

    _metadata_cls: Type[BaseProvMeta] = PrivateAttr(default=BaseProvMeta)
    _enabled: bool = PrivateAttr(default=True)

    # TODO: ideally we would make these fields 'frozen',
    # these should not be modified directly by the user.
    # instead, the user should use get_initial(), get_current()...
    # (still, we must be able to modify them using some methods)
    entity_id: UUID = Field(default_factory=lambda: uuid4())
    initial: State
    changes: List[Tuple[Patch, BaseProvMeta]] = []
    current: State

    @classmethod
    def create(cls, initial: State, *, enabled: Optional[bool] = None) -> BaseProvTracker:
        """Create a new prov-tracked object from passed initial state."""
        ret = cls(initial=initial, current=initial)
        ret._enabled = enabled if enabled is not None else cls._enabled
        return ret

    @property
    def enabled(self) -> bool:
        """Indicate whether the change tracking is enabled."""
        return self._enabled

    @enabled.setter
    def enabled(self, val: bool):
        """Enable or disable the provenance tracking.

        When disabled, calling `update` will not create a new patch.
        """
        self._enabled = val

    def update(self, new_val: State, *, metadata: Optional[BaseProvMeta] = None) -> State:
        """Update the current state, adding a diff to the previous state.

        No effect if the context is disabled (just returns passed value back).
        """
        if self.enabled:
            meta = metadata or self._metadata_cls()
            patch = (self.diff(self.current, new_val), meta)
            self.changes.append(patch)

        self.current = new_val
        return new_val

    def get_initial(self) -> State:
        """Return a deep copy of the current state.

        Always use this when you plan to apply and track changes and are not
        sure whether the operations you do will affect the original object.
        """
        return deepcopy(self.initial)

    def get_current(self) -> State:
        """Return a deep copy of the current state.

        Always use this when you plan to apply and track changes and are not
        sure whether the operations you do will affect the original object.
        """
        return deepcopy(self.current)

    def _check(self):
        """Check whether the current state is result of the diff sequence.

        If this fails, there must be some implementation error.
        """
        result = functools.reduce(self.apply, map(lambda x: x[0], self.changes), self.get_initial())
        if result != self.get_current():
            msg = 'Patch sequence does not produce current state!'
            raise RuntimeError(msg)

    # ----
    # to be implemented for provenance-tracked types:

    @staticmethod
    def diff(val: State, val_new: State) -> Patch:
        """Compute difference between two states"""
        raise NotImplementedError

    @staticmethod
    def apply(val: State, diff: Patch) -> State:
        """Apply a patch to a state and return new state."""
        raise NotImplementedError


def _find_tracker_arg(tracker_cls: Type[BaseProvTracker], args, kwargs) -> Union[int, str]:
    """Find prov tracker object passed into a function as argument."""
    ph: Optional[Union[int, str]] = None
    for key, arg in itertools.chain(enumerate(args), kwargs.items()):
        if isinstance(arg, tracker_cls):
            if ph is None:
                ph = key
            else:
                ph = None
                break
    if ph is None:
        msg = f'Some {tracker_cls.__name__} '
        msg += 'must be passed exactly once to the function!'
        raise ValueError(msg)
    return ph


def _get_arg(i: Union[int, str], a, k):
    """Get an argument from either args or kwargs."""
    return a[i] if isinstance(i, int) else k[i]


def _set_arg(i, v, a, k):
    """Set an argument in either args or kwargs."""
    (a if isinstance(i, int) else k)[i] = v


def handle_tracker_arg(tracker_cls: Type[BaseProvTracker], args, kwargs):
    """Substitute tracker context in arguments with current state."""
    arg_key: Union[int, str] = _find_tracker_arg(tracker_cls, args, kwargs)
    tracker_obj = _get_arg(arg_key, args, kwargs)
    _set_arg(arg_key, tracker_obj.get_current(), args, kwargs)
    return (tracker_obj, args, kwargs)


def with_prov(tracker_cls: Type[BaseProvTracker], raw_func, args, kwargs):
    """Perform a computation while tracking the difference and some metadata.

    Usually you will not call this directly, instead this is called
    from functions decorated by `add_tracker`.

    Requirements for the function:
        * an object of the type tracker_cls must be in (kw)args exactly once.
        * The result must be of the same type as tracked by tracker_cls.

    Args:
        tracker_cls: The prov tracker subclass to use
        raw_func: A raw (i.e., unwrapped) function to be executed
        args: Positional args for the function
        kwargs: Keyword args for the function
    """
    # substitute the tracker object with the current state ('real' argument)
    if not isinstance(args, list):
        args = list(args)
    tracker_obj, args, kwargs = handle_tracker_arg(tracker_cls, args, kwargs)
    # obtain general provenance metadata about called function
    metadata_cls = tracker_obj._metadata_cls
    metadata = metadata_cls.from_object(raw_func)
    # compute result, sanity-check the result
    tracker_state_t = type(tracker_obj.current)
    result = raw_func(*args, **kwargs)
    if not isinstance(result, tracker_state_t):
        msg = f"Wrapped function '{raw_func.__qualname__}' "
        msg += 'did not return the expected object of type '
        msg += f"'{tracker_state_t.__qualname__}', cannot compute patch!"
        raise TypeError(msg)
    # compute patch and update tracker object
    tracker_obj.update(result, metadata=metadata)
    # NOTE: returning back the tracker object allows to e.g. nest functions,
    # i.e., `f.with_prov(g.with_prov(x))` where `x` is some tracker object.
    return tracker_obj


def tracker_wrapper(tracker_cls: Type[BaseProvTracker]):
    """Create function wrapper class for the given prov tracker class."""

    class BoundFuncProvWrapper(wrapt.BoundFunctionWrapper):  # type: ignore
        def __call__(self, *args, **kwargs):
            return super(BoundFuncProvWrapper, self).__call__(*args, **kwargs)

        def with_prov(self, *args, **kwargs):
            return with_prov(tracker_cls, self.__wrapped__, args, kwargs)

    class FuncProvWrapper(wrapt.FunctionWrapper):  # type: ignore
        __bound_function_wrapper__ = BoundFuncProvWrapper

        def __init__(self, *args, **kwargs):
            super(FuncProvWrapper, self).__init__(*args, **kwargs)
            self._self_tracker_cls = tracker_cls

        def __call__(self, *args, **kwargs):
            return super(FuncProvWrapper, self).__call__(*args, **kwargs)

        def with_prov(self, *args, **kwargs):
            return with_prov(tracker_cls, self.__wrapped__, args, kwargs)

    return FuncProvWrapper


def add_tracker(cls: Type[BaseProvTracker]):
    if not isinstance(cls, type) or not issubclass(cls, BaseProvTracker):
        msg = f'Tracker must be a subclass of {BaseProvTracker.__qualname__}!'
        raise TypeError(msg)

    @wrapt.decorator(proxy=tracker_wrapper(cls))
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


# ----

if __name__ == '__main__':  # Usage example (run in terminal to see output)
    # TODO: turn the following examples into pytest test cases

    class IntTracker(BaseProvTracker[int, int]):
        """Example demonstrating how to implement provenance tracking for a type.

        The tracked object here is an int, a patch is also an int,
        and the diff operation is just int subtraction.
        """

        # NOTE: we can also override the prov metadata class with a subclass here:
        # _metadata_cls: Type[BaseProvMeta] = PrivateAttr(default=CustomProvMeta)

        @staticmethod
        def diff(from_val: int, to_val: int) -> int:
            return to_val - from_val

        @staticmethod
        def apply(from_val: int, diff: int) -> int:
            return from_val + diff

    @add_tracker(IntTracker)
    def add(x: int, y: int) -> int:
        return x + y

    @add_tracker(IntTracker)
    def mul(x: int, y: int) -> int:
        return x * y

    class MyClass:
        @add_tracker(IntTracker)
        def inc(self, *, value: int) -> int:
            return value + 1

    # wrapped functions can still work normally:
    print('1 + 2 =', add(1, 2))

    # if we use `.with_prov` and pass a wrapped input, the computation is tracked:
    x = IntTracker.create(5)
    result = mul.with_prov(3, add.with_prov(x, 4))  # we can even nest!
    print(f'3 * (<5> + 4) = {result.get_current()} (with tracking the {result.get_initial()})')

    # we can serialize the prov-tracked value...
    prov = result.model_dump_json(indent=4, exclude_defaults=True)
    print('tracked patch and provenance sequence:')
    print(prov)

    # ... later load it and continue computing
    x2 = IntTracker.model_validate_json(prov)
    MyClass().inc.with_prov(value=x2)  # also works with kwargs + class methods!
    print('after increment:')
    print(x2.model_dump_json(indent=4, exclude_defaults=True))

    # we can disable the tracking with enabled=False (also accepted by `.create`)
    # this allows to toggle execution with or without prov tracking,
    # without the need to modify code in more than one place.
    x2.enabled = False
    add.with_prov(x2, 10)
    print('after adding 10 (note that the last `add` was not tracked):')
    print(x2.model_dump_json(indent=4, exclude_defaults=True))

    @add_tracker(IntTracker)
    def invalid(x):
        return 'surprise!'

    # this will fail because the returned type does not match:
    print('brace yourself for a stacktrace:')
    invalid.with_prov(IntTracker.create(5))
