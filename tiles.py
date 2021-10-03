#!/usr/bin/env python3


from aiohttp import web

from common.network import create_session, close_session
from common.tiles import get_tile

routes = web.RouteTableDef()

# Web Mercator is the projection of reference, and the Google tile scheme is the tile extent convention of reference.
@routes.get("/{z}/{x}/{y}.png")
async def tile(request):
    global cache
    z = int(request.match_info["z"])
    x = int(request.match_info["x"])
    y = int(request.match_info["y"])
    session = request.app["MY_PERSISTENT_SESSION"]
    raster = await get_tile(z, x, y, session)
    return web.Response(body=raster, content_type="image/png")


app = web.Application()
app.on_startup.append(create_session)
app.on_shutdown.append(close_session)

app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app)
