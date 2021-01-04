import asyncio
import sys

import aiohttp
from aiohttp import ClientSession


async def fetch_status(session: ClientSession, url: str) -> int:
    ten_millis = aiohttp.ClientTimeout(total=.01)
    async with session.get(url, timeout=ten_millis) as result:
        return result.status


async def main(urls):
    session_timeout = aiohttp.ClientTimeout(total=1, connect=.1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        tasks = [fetch_status_code(session, url) for url in urls] 
        results = await asyncio.gather(*tasks, return_exceptions=True)
        exceptions = [res for res in results if isinstance(res, Exception)] 
        successful_results = [res for res in results if not isinstance(res, Exception)]
        print(f'All results: {results}')
        print(f'Finished successfully: {successful_results}') 
        print(f'Threw exceptions: {exceptions}')


asyncio.run(main(sys.argv[1:]))
