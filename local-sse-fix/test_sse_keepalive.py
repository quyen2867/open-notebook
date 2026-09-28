import asyncio
import importlib.util
import unittest

spec = importlib.util.spec_from_file_location('keepalive', '/app/api/routers/_sse_keepalive.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
stream_with_heartbeats = module.stream_with_heartbeats

class HeartbeatTests(unittest.IsolatedAsyncioTestCase):
    async def test_slow_producer_keeps_running_once_and_preserves_events(self):
        calls = []
        async def events():
            calls.append('start')
            yield 'data: user\n\n'
            await asyncio.sleep(.06)
            calls.append('answer')
            yield 'data: answer\n\n'
            yield 'data: complete\n\n'
        result = [event async for event in stream_with_heartbeats(events(), .01)]
        self.assertGreaterEqual(result.count(': keepalive\n\n'), 3)
        self.assertEqual([x for x in result if x.startswith('data:')],
                         ['data: user\n\n', 'data: answer\n\n', 'data: complete\n\n'])
        self.assertEqual(calls, ['start', 'answer'])

    async def test_producer_failure_propagates(self):
        async def events():
            await asyncio.sleep(.02)
            raise ValueError('producer failed')
            yield ''
        with self.assertRaisesRegex(ValueError, 'producer failed'):
            async for _ in stream_with_heartbeats(events(), .005):
                pass

    async def test_disconnect_cleans_up_pending_producer(self):
        closed = asyncio.Event()
        async def events():
            try:
                await asyncio.Event().wait()
                yield 'never'
            finally:
                closed.set()
        stream = stream_with_heartbeats(events(), .01)
        self.assertEqual(await anext(stream), ': keepalive\n\n')
        await stream.aclose()
        self.assertTrue(closed.is_set())

    async def test_empty_stream_finishes_without_heartbeat(self):
        async def events():
            if False:
                yield ''
        self.assertEqual([x async for x in stream_with_heartbeats(events())], [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
