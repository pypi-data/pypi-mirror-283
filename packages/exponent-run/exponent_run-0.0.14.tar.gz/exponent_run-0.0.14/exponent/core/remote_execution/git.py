import os
from collections.abc import Callable
from pathlib import Path

import pygit2
from exponent.core.remote_execution.types import (
    GetAllTrackedFilesRequest,
    GetAllTrackedFilesResponse,
    GitInfo,
    RemoteFile,
)
from pygit2 import Repository, Tree


def get_all_tracked_files(
    request: GetAllTrackedFilesRequest,
    working_directory: str,
) -> GetAllTrackedFilesResponse:
    return GetAllTrackedFilesResponse(
        correlation_id=request.correlation_id,
        files=get_all_tracked_git_file_paths(working_directory),
    )


def get_all_tracked_git_file_paths(working_directory: str) -> list[RemoteFile]:
    working_path = Path(working_directory).resolve()
    repo = pygit2.Repository(working_directory)

    paths: list[str] = []
    for path in get_tracked_files_in_dir(repo, working_directory):
        resolved_path = Path(path).resolve()
        relative_path = resolved_path.relative_to(working_path)
        paths.append(str(relative_path))

    return [
        RemoteFile(file_path=path, working_directory=working_directory)
        for path in sorted(paths)
    ]


def get_git_info(working_directory: str) -> GitInfo | None:
    try:
        repo = pygit2.Repository(working_directory)
    except pygit2.GitError:
        return None

    return GitInfo(
        branch=_get_git_branch(repo) or "<unknown branch>",
        remote=_get_git_remote(repo),
    )


def get_tracked_files_in_dir(
    repo: Repository, dir: str | Path, filter_func: Callable[[str], bool] | None = None
) -> list[str]:
    rel_path = get_path_relative_to_repo_root(repo, dir)
    dir_tree = get_git_subtree_for_dir(repo, dir)
    entries: list[str] = []
    for entry in dir_tree:
        if not entry.name:
            continue
        entry_path = f"{repo.workdir}/{rel_path}/{entry.name}"
        if entry.type_str == "tree":
            entries.extend(get_tracked_files_in_dir(repo, entry_path, filter_func))
        elif entry.type_str == "blob":
            if not filter_func or filter_func(entry.name):
                entries.append(entry_path)
    return entries


def get_git_subtree_for_dir(repo: Repository, dir: str | Path) -> Tree:
    rel_path = get_path_relative_to_repo_root(repo, dir)

    head_commit = repo.head.peel()
    head_tree: Tree = head_commit.tree

    if rel_path == Path("."):
        # If the relative path is the root of the repo, then
        # the head_tree is what we want. Note we do this because
        # Passing "." or "" as the path into the tree will raise.
        return head_tree
    return head_tree[str(rel_path)]


def get_path_relative_to_repo_root(repo: Repository, path: str | Path) -> Path:
    path = Path(path).resolve()
    return path.relative_to(Path(repo.workdir).resolve())


def _get_git_remote(repo: pygit2.Repository) -> str | None:
    if repo.remotes:
        return str(repo.remotes[0].url)
    return None


def _get_git_branch(repo: pygit2.Repository) -> str | None:
    try:
        # Look for HEAD file in the .git directory
        head_path = os.path.join(repo.path, "HEAD")
        with open(head_path) as head_file:
            # The HEAD file content usually looks like: 'ref: refs/heads/branch_name'
            head_content = head_file.read().strip()
            if head_content.startswith("ref:"):
                return head_content.split("refs/heads/")[-1]
            else:
                return None
    except Exception:  # noqa: BLE001
        return None
