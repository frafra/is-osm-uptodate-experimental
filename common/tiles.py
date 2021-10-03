import asyncio

from matplotlib import cm

import mercantile
import png

import io

#from providers.osm import get_data
from providers.ohsome import get_data
#from providers.overpass import get_data

Z_MAX = 19
#Z_EXTRA = 2  # Tile splitted in 4**Z_EXTRA subtiles/pixels
Z_EXTRA = 2


def tile_recursive(z_target, *tiles):
    for tile in tiles:
        if tile.z >= z_target:
            yield tile
        else:
            yield from tile_recursive(z_target, *mercantile.children(tile))


def base_tiles_bbox(x, y, z, z_target=Z_MAX + Z_EXTRA):
    tile = mercantile.Tile(x, y, z)
    for tile in tile_recursive(z_target, tile):
        yield mercantile.bounds(tile)


async def get_value(z, x, y, session):
    #loop = asyncio.get_event_loop()
    #values = []
    #for bbox in await loop.run_in_executor(None, base_tiles_bbox, x, y, z + Z_EXTRA):
    #    result = await get_data(session, bbox)
    #    values.append(result["versions_avg"])
    #avg = sum(values) / len(values)
    tile = mercantile.Tile(x, y, z+1)
    avg = (await get_data(session, mercantile.bounds(tile)))["versions_avg"]
    if avg > 3:
        avg = 3
    value = 255 - round((3 - avg) * (255 / (3 - 1)))
    return value


viridis = cm.get_cmap("viridis", 256)


async def get_tile(z, x, y, session, cache={}):
    tile = io.BytesIO()
    writer = png.Writer(1, 1, greyscale=False)
    value = await get_value(z, x, y, session)
    writer.write(tile, [[round(c * 255) for c in viridis(value)[:3]]])
    tile.seek(0)
    return tile.read()


"""
def coordinates_to_bbox(x, y, z):
    return mercantile.bounds(mercantile.Tile(x, y, z))

def get_tiles(z, x, y):
    if z < 1 or z > 19:
        return None  # invalid
    if z == 19:
        return [[z, x, y]]
    return (
        get_tiles(z + 1, 2 * x, 2 * y)
        + get_tiles(z + 1, 2 * x + 1, 2 * y)
        + get_tiles(z + 1, 2 * x, 2 * y + 1)
        + get_tiles(z + 1, 2 * x + 1, 2 * y + 1)
    )

mercantile.children(Tile(x, y, z))
"""
