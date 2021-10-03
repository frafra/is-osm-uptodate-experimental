from common.network import fetch

import collections

URL = "https://api.ohsome.org/v1/elementsFullHistory/bbox"

META = "https://api.ohsome.org/v1/metadata"

async def get_data(session, bbox):
    """
    metadata = await fetch(
        session,
        META,
    )
    temporal_extent = metadata["extractRegion"]["temporalExtent"]
    start = temporal_extent["fromTimestamp"]
    end = temporal_extent["toTimestamp"]
    print(start)
    print(end)
    """
    start="2007-10-08T00:00:00Z"
    end="2021-05-02T19:00Z"


    # users_total = 0
    last = ""
    first = "_"
    tasks = []

    response_bbox = await fetch(
        session,
        URL,
        params={
            "bboxes": f"{bbox.west},{bbox.south},{bbox.east},{bbox.north}",
            "properties": "metadata",
            "showMetadata": "false",
            "time": f"{start},{end}",
            "types": "node",
        },
    )

    print(len(response_bbox["features"]))

    nodes_revisions = collections.defaultdict(int)
    for feature in response_bbox["features"]:
        osm_id = feature["properties"]["@osmId"]
        nodes_revisions[osm_id] += 1
    
    if nodes_revisions:
        versions_avg = sum(nodes_revisions.values())/len(nodes_revisions)
    else:
        versions_avg = 1
    return {
        "versions_avg": versions_avg,
    }
