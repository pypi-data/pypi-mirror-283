from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str


class DetailedSearchResult(SearchResult):
    detail: str | None = None
