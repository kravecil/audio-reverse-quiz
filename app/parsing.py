import re

from bs4 import BeautifulSoup

from app.schemas import PaginationLinkSchema, TrackSchema

REGEXP_LAST_START_FROM = r"\/search\/start\/(?P<last_start_from>\d+)\?q=(?P<q>.+)"
LINK_PATTERN = "/search/start/{last_start_from}?q={q}"
PER_PAGE_SIZE = 48


class ParsingService:
    soup: BeautifulSoup

    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, features="html.parser")

    def get_track_list(self) -> list[TrackSchema]:
        tracks: list[TrackSchema] = []

        track_list = self.soup.find(class_="tracks__list")
        if track_list is None:
            return tracks

        track_tags = track_list.find_all(class_="track__info")  # type: ignore
        if track_tags is None:
            return tracks

        for track_tag in track_tags:
            track_info = track_tag.find(class_="track__info-l")

            title: str = track_info.find(class_="track__title").string
            desc: str = track_info.find(class_="track__desc").string
            href: str = track_tag.find(class_="track__download-btn").attrs.get("href")

            tracks.append(
                TrackSchema(title=title.strip(), desc=desc.strip(), href=href)
            )

        return tracks

    def get_pagination_links(self) -> list[PaginationLinkSchema] | None:
        links: list[str] = []

        pagination_tag_list = self.soup.find(class_="pagination__list")
        if pagination_tag_list is None:
            return None

        pagination_last_tag = pagination_tag_list.find(  # type: ignore
            "a", class_="pagination__link", string=">>"
        )
        if pagination_last_tag:
            href = pagination_last_tag["href"]
            s = re.search(REGEXP_LAST_START_FROM, href)
            if s is None:
                return None

            links.extend(
                self.generate_links_by_last_page(
                    int(s.group("last_start_from")), s.group("q")
                )
            )
        else:
            link_tags = pagination_tag_list.find_all("a", class_="pagination__link")  # type: ignore
            links.extend([tag["href"] for tag in link_tags])

        if not len(links):
            return None

        return [
            PaginationLinkSchema(title=str(idx + 1), link=link)
            for idx, link in enumerate(links)
        ]

    @staticmethod
    def generate_links_by_last_page(last_start_from: int, q: str) -> list[str]:
        links = [
            LINK_PATTERN.format(last_start_from=r, q=q)
            for r in range(
                PER_PAGE_SIZE, last_start_from + PER_PAGE_SIZE, PER_PAGE_SIZE
            )
        ]
        return links
