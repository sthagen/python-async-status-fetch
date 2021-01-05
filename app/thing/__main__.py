import asyncio
import os
import sys

import aiohttp
from aiohttp import ClientSession

BATCH_TOTAL_TIMEOUT_SECS = float(os.getenv("BATCH_TOTAL_TIMEOUT_SECS", 1.))
BATCH_CONNECT_TIMEOUT_SECS = float(os.getenv("BATCH_CONNECT_TIMEOUT_SECS", .1))
BATCH_GET_TIMEOUT_SECS = float(os.getenv("BATCH_GET_TIMEOUT_SECS", 1.))


async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=BATCH_GET_TIMEOUT_SECS)) as result:
        return result.status


async def main(urls):
    session_timeout = aiohttp.ClientTimeout(total=BATCH_TOTAL_TIMEOUT_SECS, connect=BATCH_CONNECT_TIMEOUT_SECS)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        tasks = [fetch_status(session, url) for url in urls] 
        results = await asyncio.gather(*tasks, return_exceptions=True)
        exceptions = [res for res in results if isinstance(res, Exception)] 
        successful_results = [res for res in results if not isinstance(res, Exception)]
        print(f'All results: {results}')
        print(f'Status OK:  {successful_results}') 
        print(f'Status NOK: {exceptions}')


asyncio.run(main(sys.argv[1:]))
