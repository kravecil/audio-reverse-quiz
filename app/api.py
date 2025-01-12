import asyncio
from functools import reduce

import httpx
from fastapi import APIRouter

from app.parsing import get_results

api = APIRouter()

SOURCE_HOST_URL = r"https://rus.hitmotop.com"


async def get_html(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return response.text


async def get_tracks_task(url: str):
    html = await get_html(url)
    track_list = get_results(html)

    return track_list


@api.get("/api/get-tracks")
async def get_tracks(q: str):
    base_url = f"{SOURCE_HOST_URL}/search?q={q}"

    html = await get_html(base_url)
    tracks, links = get_results(html, with_links=True)

    tasks = [
        asyncio.create_task(get_tracks_task(f"{SOURCE_HOST_URL}{link}"))
        for link in links
    ]
    results = await asyncio.gather(*tasks)
    tracks.extend(reduce(lambda sum, val: sum + val[0], results, []))

    return tracks
