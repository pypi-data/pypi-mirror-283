# -*- coding: utf-8 -*-
from data_harvesting.stats.config import REPOSITORY_URL, REPOSITORY_BRANCH, GIT_USERNAME, GIT_TOKEN, GIT_EMAIL, GIT_FOLDER
from prefect import get_run_logger
import pygit2
from prefect import task
from datetime import datetime


class MyRemoteCallbacks(pygit2.RemoteCallbacks):  # type: ignore
    def credentials(self, url, username_from_url, allowed_types):
        return pygit2.UserPass(GIT_USERNAME, GIT_TOKEN)


@task(persist_result=True, log_prints=True, task_run_name='clone-repository')
def clone_repository():
    logger = get_run_logger()

    if not REPOSITORY_URL:
        logger.error('Repository URL is not set.')
        return

    if not GIT_USERNAME or not GIT_TOKEN:
        logger.error('Git credentials are not set.')
        return

    logger.info(f'Cloning the repository {REPOSITORY_URL} on branch {REPOSITORY_BRANCH}.')

    # clone the repository
    pygit2.clone_repository(REPOSITORY_URL, GIT_FOLDER, checkout_branch=REPOSITORY_BRANCH, callbacks=MyRemoteCallbacks())


@task(persist_result=True, log_prints=True, task_run_name='commit-and-push')
def commit_and_push():
    logger = get_run_logger()

    # check if repository folder exists, if not, clone the repository
    if not GIT_FOLDER.exists():
        logger.info('Repository folder does not exist.')
        clone_repository()

    logger.info('Committing and pushing the changes to the repository.')

    if not GIT_USERNAME or not GIT_EMAIL or not GIT_TOKEN:
        logger.error('Git credentials are not set.')
        return

    # open the repository
    repo = pygit2.Repository(GIT_FOLDER)

    # create the index
    index = repo.index
    index.add_all()
    index.write()

    # create the tree
    tree = index.write_tree()

    # create the author
    author = pygit2.Signature(GIT_USERNAME, GIT_EMAIL)

    # create the committer
    committer = pygit2.Signature(GIT_USERNAME, GIT_EMAIL)

    message = f'Updated statistics for {datetime.now().strftime("%Y-%m-%d")}'

    # create the commit
    oid = repo.create_commit('HEAD', author, committer, message, tree, [repo.head.target])
    logger.info(f'Created commit {oid}')

    # push the changes
    repo.head.set_target(oid)
    remote = repo.remotes['origin']
    remote.push([repo.head.name], callbacks=MyRemoteCallbacks())
    logger.info('Pushed the changes to the repository.')
