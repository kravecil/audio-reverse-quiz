import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.parsing import ParsingService
from app.schemas import TrackListSchema
from app.settings import SOURCE_HOST_URL

api = APIRouter(prefix="/api")


async def get_html(url: str):
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url)

    return response.text


@api.get("/tracks")
async def get_tracks(q: str, start: int | None = None) -> TrackListSchema:
    base_url = f"{SOURCE_HOST_URL}/search/start/{start or 1}?q={q}"

    html = await get_html(base_url)

    service = ParsingService(html=html)

    tracks = service.get_track_list()

    links = service.get_pagination_links() if start is None else None

    return TrackListSchema(tracks=tracks, links=links)


@api.get("/track")
def get_track(url: str) -> StreamingResponse:
    def get_stream():
        with httpx.stream("GET", url, follow_redirects=True) as stream:
            yield from stream.iter_bytes()

    return StreamingResponse(get_stream())
