import logging
import os

from diff_match_patch import diff_match_patch
from exponent.core.remote_execution.types import (
    WRITE_STRATEGY_FULL_FILE_REWRITE,
    WRITE_STRATEGY_UDIFF,
    FileWriteRequest,
    FileWriteResponse,
)
from exponent.core.remote_execution.utils import assert_unreachable

logger = logging.getLogger(__name__)


def execute_file_write(
    request: FileWriteRequest, working_directory: str
) -> FileWriteResponse:
    write_strategy = request.write_strategy
    if write_strategy == WRITE_STRATEGY_FULL_FILE_REWRITE:
        result = execute_full_file_rewrite(
            request.file_path, request.content, working_directory
        )
    elif write_strategy == WRITE_STRATEGY_UDIFF:
        result = execute_udiff_edit(
            request.file_path, request.content, working_directory
        )
    else:
        assert_unreachable(write_strategy)
    return FileWriteResponse(
        content=result,
        correlation_id=request.correlation_id,
    )


def execute_full_file_rewrite(
    file_path: str, content: str, working_directory: str
) -> str:
    try:
        # Construct the absolute path
        full_file_path = os.path.join(working_directory, file_path)

        # Check if the directory exists, if not, create it
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        # Determine if the file exists and write the new content
        if os.path.exists(full_file_path):
            with open(full_file_path, "w") as file:
                file.write(content)
            return f"Modified file {file_path}"
        else:
            with open(full_file_path, "w") as file:
                file.write(content)
            return f"Created file {file_path}"

    except Exception as e:  # noqa: BLE001
        return f"An error occurred: {e!s}"


def execute_udiff_edit(file_path: str, content: str, working_directory: str) -> str:
    try:
        # Construct the absolute path
        full_file_path = os.path.join(working_directory, file_path)

        # Check if the directory exists, if not, create it
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        # Determine if the file exists and write the new content
        if os.path.exists(full_file_path):
            success = open_file_and_apply_udiff(full_file_path, content)
            if success:
                return f"Modified file {file_path}"
            else:
                return f"Failed to modify file {file_path}"
        else:
            success = open_file_and_apply_udiff(full_file_path, content)
            if success:
                return f"Created file {file_path}"
            else:
                return f"Failed to create file {file_path}"

    except Exception as e:
        raise e


def open_file_and_apply_udiff(file_path: str, diff: str) -> bool:
    with open(file_path) as file:
        content = file.read()

    new_content = apply_udiff(content, diff)
    if new_content is None:
        return False

    with open(file_path, "w") as file:
        file.write(new_content)

    return True


def apply_udiff(existing_content: str, diff_content: str) -> str | None:
    hunks = get_raw_udiff_hunks(diff_content)
    for hunk in hunks:
        if not hunk:
            continue
        print(f"Applying hunk: {hunk[0][:100]}...")
        search, replace = split_hunk_for_search_and_replace(hunk)
        # Try simple search and replace first
        new_content = simple_search_and_replace(existing_content, search, replace)
        if new_content:
            existing_content = new_content
            continue
        # Simple search and replace failed, try fancy instead
        new_content = diff_patch_search_and_replace(existing_content, search, replace)
        if new_content is None:
            print("Failed to apply hunk, exiting!")
            return None
        print("Applied successfully!")
        existing_content = new_content
    return existing_content


def get_raw_udiff_hunks(content: str) -> list[list[str]]:
    lines = content.splitlines(keepends=True)
    hunks: list[list[str]] = []
    current_hunk: list[str] = []
    for line in lines:
        if line.startswith("@@"):
            if current_hunk:
                hunks.append(current_hunk)
                current_hunk = []
        else:
            current_hunk.append(line)
    if current_hunk:
        hunks.append(current_hunk)
    return hunks


def split_hunk_for_search_and_replace(hunk: list[str]) -> tuple[str, str]:
    search_lines = []
    replace_lines = []

    search_prefixes = ["-", " "]
    replace_prefixes = ["+", " "]
    for line in hunk:
        if not line:
            continue
        prefix, content = line[0], line[1:]
        if not content:
            continue
        if prefix in search_prefixes:
            search_lines.append(content)
        if prefix in replace_prefixes:
            replace_lines.append(content)
    return "".join(search_lines), "".join(replace_lines)


def simple_search_and_replace(content: str, search: str, replace: str) -> str | None:
    if content.count(search) == 1:
        return content.replace(search, replace)
    return None


def diff_patch_search_and_replace(
    content: str, search: str, replace: str
) -> str | None:
    patcher = diff_match_patch()
    # 3 second tieout for computing diffs
    patcher.Diff_Timeout = 3
    patcher.Match_Threshold = 0.95
    patcher.Match_Distance = 500
    patcher.Match_MaxBits = 128
    patcher.Patch_Margin = 32
    search_vs_replace_diff = patcher.diff_main(search, replace, False)

    # Simplify the diff as much as possible
    patcher.diff_cleanupEfficiency(search_vs_replace_diff)
    patcher.diff_cleanupSemantic(search_vs_replace_diff)

    original_vs_search_diff = patcher.diff_main(search, content)
    new_diffs = patcher.patch_make(search, search_vs_replace_diff)
    # Offset the search vs. replace diffs with the offset
    # of the search diff within the original content.
    for new_diff in new_diffs:
        new_diff.start1 = patcher.diff_xIndex(original_vs_search_diff, new_diff.start1)
        new_diff.start2 = patcher.diff_xIndex(original_vs_search_diff, new_diff.start2)

    new_content, successes = patcher.patch_apply(new_diffs, content)
    if not all(successes):
        return None

    return str(new_content)
