"""Keep SSE transports alive while their producer waits for a model response."""

import asyncio
from contextlib import suppress
from typing import AsyncIterator


async def stream_with_heartbeats(
    events: AsyncIterator[str], interval: float = 10.0
) -> AsyncIterator[str]:
    pending = None
    try:
        while True:
            if pending is None:
                pending = asyncio.create_task(anext(events))
            done, _ = await asyncio.wait({pending}, timeout=interval)
            if not done:
                # SSE comments keep the connection alive without adding chat text.
                yield ": keepalive\n\n"
                continue
            completed = pending
            pending = None
            try:
                event = completed.result()
            except StopAsyncIteration:
                break
            yield event
    finally:
        if pending is not None:
            pending.cancel()
            with suppress(asyncio.CancelledError, StopAsyncIteration):
                await pending
        close = getattr(events, "aclose", None)
        if close is not None:
            await close()
