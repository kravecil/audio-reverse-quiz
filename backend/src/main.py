import asyncio
import re
from functools import reduce

import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

SOURCE_HOST_URL = r"https://rus.hitmotop.com"
REGEXP_LAST_START_FROM = r"\/search\/start\/(?P<last_start_from>\d+)\?q=(?P<q>.+)"
LINK_PATTERN = "/search/start/{last_start_from}?q={q}"
PER_PAGE_SIZE = 48


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


def generate_links_by_last_page(last_start_from: int, q: str):
    links = [
        LINK_PATTERN.format(last_start_from=r, q=q)
        for r in range(PER_PAGE_SIZE, last_start_from + PER_PAGE_SIZE, PER_PAGE_SIZE)
    ]
    return links


def get_pagination_links(soup: BeautifulSoup):
    links = []

    pagination_list_tag = soup.find(class_="pagination__list")
    if pagination_list_tag is None:
        return links

    pagination_last_tag = pagination_list_tag.find(
        "a", class_="pagination__link", string=">>"
    )
    if pagination_last_tag:
        href = pagination_last_tag["href"]
        s = re.search(REGEXP_LAST_START_FROM, href)
        if s is None:
            return links

        links.extend(
            generate_links_by_last_page(int(s.group("last_start_from")), s.group("q"))
        )
    else:
        link_tags = pagination_list_tag.find_all("a", class_="pagination__link")
        links.extend([tag["href"] for tag in link_tags])

    return links


def parse_result(text: str):
    soup = BeautifulSoup(text, features="html.parser")

    tracks = get_track_list(soup)
    links = get_pagination_links(soup)

    return tracks, links


async def get_web(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    return response.text


async def get_results(url: str):
    html = await get_web(url)
    tracks, links = parse_result(html)

    return tracks, links


@app.get("/api/get-tracks")
async def get_tracks(q: str):
    tracks, links = await get_results(f"{SOURCE_HOST_URL}/search?q={q}")

    tasks = [
        asyncio.create_task(get_results(f"{SOURCE_HOST_URL}{link}")) for link in links
    ]
    results = await asyncio.gather(*tasks)
    tracks.extend(reduce(lambda sum, val: sum + val[0], results, []))

    return tracks
