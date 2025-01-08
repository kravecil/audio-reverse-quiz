import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

SOURCE_HOST_URL = r"https://rus.hitmotop.com"


def get_track_list(soup: BeautifulSoup):
    tracks = []

    track_tags = soup.find(class_="tracks__list").find_all(class_="track__info")
    if track_tags is None:
        return tracks

    for track_tag in track_tags:
        track_info = track_tag.find(class_="track__info-l")

        title: str = track_info.find(class_="track__title").string
        desc: str = track_info.find(class_="track__desc").string
        filepath: str = track_tag.find(class_="track__download-btn").attrs.get("href")

        tracks.append(
            {
                "title": title.strip(),
                "desc": desc.strip(),
                "filepath": filepath,
            }
        )

    return tracks


def get_pagination_links(soup: BeautifulSoup):
    links = []

    pagination_list_tag = soup.find(class_="pagination__list")
    if pagination_list_tag is None:
        return links


def parse_result(text: str):
    soup = BeautifulSoup(text, features="html.parser")

    tracks = get_tracks(soup)
    links = get_pagination_links(soup)

    return tracks, links


async def get_web(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return response.text


@app.get("/api/get-tracks")
async def get_tracks(q: str):
    html = await get_web(f"{SOURCE_HOST_URL}/search?q={q}")

    tracks, links = parse_result(html)
