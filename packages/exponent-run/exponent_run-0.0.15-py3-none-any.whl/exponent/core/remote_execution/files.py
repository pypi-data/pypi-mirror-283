import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from exponent.core.remote_execution.types import (
    GetFileAttachmentRequest,
    GetFileAttachmentResponse,
    GetMatchingFilesRequest,
    GetMatchingFilesResponse,
    ListFilesRequest,
    ListFilesResponse,
    RemoteFile,
)
from gitignore_parser import (
    IgnoreRule,
    handle_negation,
    parse_gitignore,
    rule_from_pattern,
)
from rapidfuzz import process


class FileCache:
    def __init__(self, working_directory: str):
        self.working_directory = working_directory
        self._cache: list[str] | None = None

    @property
    def files(self) -> list[str]:
        if self._cache is None:
            self._cache = file_walk(self.working_directory)
        return self._cache


def list_files(list_files_request: ListFilesRequest) -> ListFilesResponse:
    filenames = os.listdir(list_files_request.directory)
    return ListFilesResponse(
        files=[
            RemoteFile(
                file_path=filename,
                working_directory=list_files_request.directory,
            )
            for filename in filenames
        ],
        correlation_id=list_files_request.correlation_id,
    )


def get_file_attachment(
    get_file_attachment_request: GetFileAttachmentRequest,
) -> GetFileAttachmentResponse:
    file_path = get_file_attachment_request.file.absolute_path
    with open(file_path) as f:
        return GetFileAttachmentResponse(
            content=f.read(),
            file=get_file_attachment_request.file,
            correlation_id=get_file_attachment_request.correlation_id,
        )


def _parse_gitignore(directory: str) -> Any:
    gitignore_path = os.path.join(directory, ".gitignore")
    if os.path.isfile(gitignore_path):
        return parse_gitignore(gitignore_path)
    return None


def _parse_ignore_extra(
    working_directory: str, ignore_extra: list[str]
) -> Callable[[str], bool]:
    rules: list[IgnoreRule] = []
    for pattern in ignore_extra:
        if (
            rule := rule_from_pattern(pattern, base_path=working_directory)
        ) is not None:
            rules.append(rule)

    def rule_handler(file_path: str) -> bool:
        nonlocal rules
        return bool(handle_negation(file_path, rules))

    return rule_handler


def _or(a: Callable[[str], bool], b: Callable[[str], bool]) -> Callable[[str], bool]:
    def or_handler(file_path: str) -> bool:
        return a(file_path) or b(file_path)

    return or_handler


def _get_ignored_checker(
    dir_path: str, existing_ignores: dict[str, Any]
) -> Callable[[str], bool] | None:
    new_ignore = _parse_gitignore(dir_path)
    existing_ignore = existing_ignores.get(dir_path)
    if existing_ignore and new_ignore:
        return _or(new_ignore, existing_ignore)
    return new_ignore or existing_ignore


def file_walk(
    working_directory: str, ignore_extra: list[str] | None = None
) -> list[str]:
    ignored_checkers = {}
    if ignore_extra:
        # Optional extra gitignore patterns
        ignored_checkers[working_directory] = _parse_ignore_extra(
            working_directory, ignore_extra
        )

    all_files = []
    for dirpath, dirnames, filenames in os.walk(working_directory):
        # Update or add new .gitignore rules when a .gitignore file is encountered
        new_ignore = _get_ignored_checker(dirpath, ignored_checkers)
        if new_ignore:
            ignored_checkers[dirpath] = new_ignore

        # Check each file in the current directory
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Check against all applicable .gitignore rules
            ignored = any(
                ignored_checkers[d](file_path)
                for d in ignored_checkers
                if file_path.startswith(d)
            )
            if not ignored:
                relative_path = os.path.relpath(file_path, working_directory)
                all_files.append(relative_path)

        # Update directory list in place to skip ignored directories
        dirnames[:] = [
            d
            for d in dirnames
            if not any(
                ignored_checkers[dp](os.path.join(dirpath, d))
                for dp in ignored_checkers
                if os.path.join(dirpath, d).startswith(dp)
            )
            and ".git" not in d
        ]

    return all_files


def get_matching_files(
    search_term: GetMatchingFilesRequest,
    file_cache: FileCache,
) -> GetMatchingFilesResponse:
    MAX_MATCHING_FILES = 10

    # Use rapidfuzz to find the best matching files
    matching_files = process.extract(
        search_term.search_term,
        file_cache.files,
        limit=MAX_MATCHING_FILES,
        score_cutoff=0,
    )

    directory = file_cache.working_directory
    files: list[RemoteFile] = []
    for file, _, _ in matching_files:
        files.append(
            RemoteFile(
                file_path=file,
                working_directory=directory,
            )
        )

    return GetMatchingFilesResponse(
        files=files,
        correlation_id=search_term.correlation_id,
    )


def normalize_files(working_directory: str, file_paths: list[str]) -> list[RemoteFile]:
    working_path = Path(working_directory).resolve()
    normalized_files = []
    for file_path in file_paths:
        relative_path = Path(file_path)
        if relative_path.is_absolute():
            relative_path = relative_path.relative_to(working_path)
        normalized_files.append(
            RemoteFile(
                file_path=str(relative_path),
                working_directory=working_directory,
            )
        )
    return sorted(normalized_files)
