import aiohttp
import asyncio

HEADERS = {
    "User-Agent": "Is-OSM-uptodate/EXPERIMENTAL_VERSION",
    "Referer": "185.71.208.252",
    "Accept-Encoding": "gzip",
}


async def create_session(app):
    conn = aiohttp.TCPConnector(limit_per_host=2)
    session = aiohttp.ClientSession(connector=conn)
    #session = aiohttp.ClientSession()
    app["MY_PERSISTENT_SESSION"] = session


async def close_session(app):
    await app["MY_PERSISTENT_SESSION"].close()


async def fetch(session, url, *args, **kwargs):
    kwargs["headers"] = kwargs.get("headers", HEADERS)
    for t in range(5):
        try:
            async with session.get(url, *args, **kwargs) as response:
                res = await response.json()
                return res
        except aiohttp.client_exceptions.ServerDisconnectedError:
            await asyncio.sleep(0.1 * 2 ** t)
        except aiohttp.client_exceptions.ContentTypeError:
            await asyncio.sleep(0.1 * 2 ** t)
    else:
        pass  # print("BIG FAIL")
