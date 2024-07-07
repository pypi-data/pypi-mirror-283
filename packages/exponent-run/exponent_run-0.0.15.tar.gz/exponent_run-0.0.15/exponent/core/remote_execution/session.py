from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from exponent.core.remote_execution.languages.python import Kernel
from exponent.core.remote_execution.utils import format_error_log
from httpx import AsyncClient


class RemoteExecutionClientSession:
    def __init__(self, working_directory: str, base_url: str, api_key: str):
        self.working_directory = working_directory
        self.api_client = AsyncClient(base_url=base_url, headers={"API-KEY": api_key})
        self.kernel = Kernel(working_directory=working_directory)

    async def log_exception(self, exc: Exception) -> None:
        error_log = format_error_log(exc)
        if not error_log:
            return
        await self.api_client.post(
            "/api/remote_execution/log_error",
            content=error_log.model_dump_json(),
            timeout=60,
        )


@asynccontextmanager
async def get_session(
    working_directory: str,
    base_url: str,
    api_key: str,
) -> AsyncGenerator[RemoteExecutionClientSession, None]:
    session = RemoteExecutionClientSession(working_directory, base_url, api_key)
    try:
        yield session
    except Exception as exc:
        await session.log_exception(exc)
        raise exc
    finally:
        session.kernel.close()
        await session.api_client.aclose()
