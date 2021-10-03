from common.network import fetch
from common.converters import iso_timestamp_to_days

import asyncio

import random

server = "https://api.openstreetmap.org"


async def get_data(session, bbox):
    nodes = 0
    versions_total = 0
    # users_total = 0
    last = ""
    first = "_"
    tasks = []

    #    connector = aiohttp.TCPConnector(limit=4)
    response_bbox = await fetch(
        session,
        f"{server}/api/0.6/map.json?bbox={bbox.west},{bbox.south},{bbox.east},{bbox.north}",
    )
    elements = [e for e in response_bbox["elements"] if e["type"] == "node"]
    random.shuffle(elements)
    for element in elements:
        nodes += 1
        versions_total += element["version"]
        if element["timestamp"] > last:
            last = element["timestamp"]
        if element["version"] == 1:
            created = element["timestamp"]
            if created < first:
                first = created
        task = asyncio.ensure_future(
            fetch(
                session,
                f"{server}/api/0.6/{element['type']}/{element['id']}/history.json",
            )
        )
        tasks.append(task)

    for task in asyncio.as_completed(tasks):
        history = await task
        if len(history["elements"]) == 0:
            continue
        created = history["elements"][0]["timestamp"]
        if created < first:
            first = created
    #    users = set((version['uid'] for version in response_history['elements']))
    #    users_total += len(users)

    if last == "":  # empty history
        return {
            "versions_avg": 1,
            "updates_freq": None,
            "last": None,
            "first": None,
        }

    first_days = iso_timestamp_to_days(first.rstrip("Z"))
    last_days = iso_timestamp_to_days(last.rstrip("Z"))
    return {
        "versions_avg": versions_total / nodes,
        "updates_freq": None,
        "last": last_days,
        "first": first_days,
    }


"""
Error handling request
Traceback (most recent call last):
  File "/home/frafra/.cache/pypoetry/virtualenvs/draft-2Uym0jAL-py3.9/lib64/python3.9/site-packages/aiohttp/web_protocol.py", line 422, in _handle_request
    resp = await self._request_handler(request)
  File "/home/frafra/.cache/pypoetry/virtualenvs/draft-2Uym0jAL-py3.9/lib64/python3.9/site-packages/aiohttp/web_app.py", line 499, in _handle
    resp = await handler(request)
  File "/home/frafra/Code/is-osm-uptodate/draft/./tiles.py", line 167, in tile
    cache[bbox] = result
  File "/home/frafra/Code/is-osm-uptodate/draft/./tiles.py", line 103, in data_osm
    if len(history['elements']) == 0:
TypeError: 'NoneType' object is not subscriptable
"""
