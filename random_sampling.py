import itertools
import random

import mercantile

Z_MAX = 19


def tile_recursive(z_target, tile):
    if tile.z >= z_target:
        yield tile
    else:
        children = mercantile.children(tile)
        random.shuffle(children)
        for child in itertools.cycle(children):
            yield from tile_recursive(z_target, child)


# https://tile.openstreetmap.org/11/1083/553.png
z = 11
x = 1083
y = 553

tile = mercantile.Tile(x, y, z)
mercantile.bounds(tile)

server = "https://api.openstreetmap.org"

session = aiohttp.ClientSession()
app["MY_PERSISTENT_SESSION"] = session


for tile in itertools.islice(tile_recursive(Z_MAX, tile), 10):
    bbox = mercantile.bounds(tile)
    url = "{server}/api/0.6/map.json?bbox={bbox.west},{bbox.south},{bbox.east},{bbox.north}"
