import re
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup

REGEXP_LAST_START_FROM = r"\/search\/start\/(?P<last_start_from>\d+)\?q=(?P<q>.+)"
LINK_PATTERN = "/search/start/{last_start_from}?q={q}"
PER_PAGE_SIZE = 48

REAL_HOST = "s3.deliciouspeaches.com"


def change_baseurl(url, base_url):
    parsed_url = list(urlparse(url))
    parsed_url[1] = REAL_HOST

    return urlunparse(parsed_url)


def get_track_list(soup: str | BeautifulSoup):
    if not isinstance(soup, BeautifulSoup):
        soup = BeautifulSoup(soup, features="html.parser")

    tracks = []

    track_list = soup.find(class_="tracks__list")
    if track_list is None:
        return tracks

    track_tags = track_list.find_all(class_="track__info")
    if track_tags is None:
        return tracks

    for track_tag in track_tags:
        track_info = track_tag.find(class_="track__info-l")

        title: str = track_info.find(class_="track__title").string
        desc: str = track_info.find(class_="track__desc").string
        # filepath: str = change_baseurl(
        #     track_tag.find(class_="track__download-btn").attrs.get("href"), REAL_HOST
        # )
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


def get_results(text: str, with_links=False):
    soup = BeautifulSoup(text, features="html.parser")

    tracks = get_track_list(soup)
    links = get_pagination_links(soup) if with_links else None

    return tracks, links


def generate_links_by_last_page(last_start_from: int, q: str):
    links = [
        LINK_PATTERN.format(last_start_from=r, q=q)
        for r in range(PER_PAGE_SIZE, last_start_from + PER_PAGE_SIZE, PER_PAGE_SIZE)
    ]
    return links
