import asyncio
import tempfile
from functools import reduce
import os

import httpx
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.parsing import get_results

api = APIRouter()

SOURCE_HOST_URL = r"https://rus.hitmotop.com"

# STORAGE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../storage"
STORAGE_PATH = "storage"


async def get_html(url: str):
    async with httpx.AsyncClient(timeout=30) as client:
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


@api.get("/api/get-track")
def get_track(url: str):
    response = httpx.get(url, follow_redirects=True)

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при получении медафайла:\n{response.text}",
        )

    with tempfile.NamedTemporaryFile(
        mode="wb", delete=False, delete_on_close=False, dir=STORAGE_PATH
    ) as f:
        f.write(response.content)
        filepath = os.path.basename(f.name)

    return filepath
