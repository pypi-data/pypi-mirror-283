import pygit2

from exponent.core.remote_execution.git import (
    get_all_tracked_files,
    get_all_tracked_git_file_paths,
    get_git_info,
    get_git_subtree_for_dir,
)
from exponent.core.remote_execution.types import (
    GetAllTrackedFilesRequest,
    GetAllTrackedFilesResponse,
    GitInfo,
    RemoteFile,
)


def get_expected_files(cwd: str) -> list[RemoteFile]:
    return sorted(
        [
            RemoteFile(
                file_path="test1.py",
                working_directory=cwd,
            ),
            RemoteFile(
                file_path="test2.py",
                working_directory=cwd,
            ),
            RemoteFile(
                file_path="exponent.txt",
                working_directory=cwd,
            ),
        ]
    )


async def test_empty_git_repo(temporary_directory_no_commit_history: str) -> None:
    expected_files = get_expected_files(temporary_directory_no_commit_history)

    repo = pygit2.Repository(temporary_directory_no_commit_history)
    subtree = get_git_subtree_for_dir(repo, temporary_directory_no_commit_history)
    assert subtree is None

    tracked_files_response = get_all_tracked_files(
        request=GetAllTrackedFilesRequest(
            correlation_id="123",
        ),
        working_directory=temporary_directory_no_commit_history,
    )
    assert tracked_files_response == GetAllTrackedFilesResponse(
        correlation_id="123",
        files=expected_files,
    )

    git_info = get_git_info(working_directory=temporary_directory_no_commit_history)
    assert git_info == GitInfo(
        branch="master",
        remote=None,
    )


async def test_non_empty_git_repo(default_temporary_directory: str) -> None:
    expected_files = get_expected_files(default_temporary_directory)

    repo = pygit2.Repository(default_temporary_directory)
    tracked_files = get_all_tracked_git_file_paths(repo, default_temporary_directory)
    assert sorted(tracked_files) == expected_files

    tracked_files_response = get_all_tracked_files(
        request=GetAllTrackedFilesRequest(
            correlation_id="123",
        ),
        working_directory=default_temporary_directory,
    )
    assert tracked_files_response == GetAllTrackedFilesResponse(
        correlation_id="123",
        files=expected_files,
    )

    git_info = get_git_info(working_directory=default_temporary_directory)
    assert git_info == GitInfo(
        branch="master",
        remote=None,
    )


async def test_non_git_repo(temporary_directory_no_git: str) -> None:
    expected_files = get_expected_files(temporary_directory_no_git)

    tracked_files_response = get_all_tracked_files(
        request=GetAllTrackedFilesRequest(
            correlation_id="123",
        ),
        working_directory=temporary_directory_no_git,
    )
    assert tracked_files_response == GetAllTrackedFilesResponse(
        correlation_id="123",
        files=expected_files,
    )

    git_info = get_git_info(working_directory=temporary_directory_no_git)
    assert git_info is None
