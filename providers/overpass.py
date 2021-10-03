from common.network import fetch

import collections

URL = "https://lz4.overpass-api.de/api/interpreter"

async def get_data(session, bbox):
    # users_total = 0
    last = ""
    first = "_"
    tasks = []

    response_bbox = await fetch(
        session,
        URL,
        params={"data": f"""
        [out:csv(::"id", ::"version", ::"timestamp")][timeout:5];
        node({bbox.south},{bbox.west},{bbox.north},{bbox.east});
        out meta;
        """},
    )
    versions = [int(v) for v in response_bbox.split()[4::3]]
    if versions:
        versions_avg = sum(versions)/len(versions)
    else:
        versions_avg = 1
    return {
        "versions_avg": versions_avg,
    }
