import asyncio


class MockStreamReader:
    def __init__(self, read_data: bytes):
        self._read_data = read_data

    async def read(self, _) -> bytes:
        return self._read_data


class MockTimeoutStreamReader:
    def __init__(self, sleep_time):
        self._sleep_time = sleep_time

    async def read(self, _) -> None:
        await asyncio.sleep(self._sleep_time)
