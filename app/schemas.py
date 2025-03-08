from pydantic import BaseModel, Field


class TrackSchema(BaseModel):
    title: str = Field(description="Исполнитель")
    desc: str = Field(description="Название композиции")
    href: str = Field(description="Гиперссылка на медиаисточник")


class PaginationLinkSchema(BaseModel):
    title: str = Field(description="Нумерация")
    link: str = Field(description="Гиперссылка на страницу запроса")


class TrackListSchema(BaseModel):
    tracks: list[TrackSchema] = Field(description="Список треков")
    links: list[PaginationLinkSchema] | None = Field(description="Пагинация")
