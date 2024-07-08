import asyncio
import json
import subprocess
from vscrapper.types import DetailedSearchResult, SearchResult
from vscrapper.utils import Utils
from vscrapper.weburl import WebURL, logger
from nest_asyncio import apply
from tempfile import TemporaryDirectory

apply()
from httpx import AsyncClient

from urllib.parse import quote_plus


class SearchQuery:

    def __init__(self, query: str, utils: Utils = Utils()):
        self.query = query
        self.url = None
        self.sanitized_url = None
        self.utils = utils

    async def google_search(self) -> list[SearchResult]:
        logger.info(f"google search")

        encoded_query = quote_plus(self.query)

        # sanitize url
        self.url = f"https://www.google.com/search?q={encoded_query}"

        self.sanitized_url = self.utils.sanitize_url(url=self.url)

        if not self.sanitized_url:
            raise Exception("Invalid URL")

        with TemporaryDirectory(prefix="temp") as tempdir:
            temp_path = f"{tempdir}/results.json"

            proc = await asyncio.subprocess.create_subprocess_shell(
                cmd=f"""npx google-it --query="{self.query}" -o {temp_path}""",
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await proc.communicate()

            with open(temp_path, "r") as f:
                results = f.read()
                results_dict = json.loads(results)

            parsed_results = []
            for res in results_dict:
                parsed_results.append(SearchResult.model_validate(res))
            return parsed_results

    async def detailed_google_search(self) -> list[DetailedSearchResult]:
        logger.info(f"detailed google search")
        search_results = await self.google_search()

        tasks = []

        for result in search_results:
            tasks.append(asyncio.create_task(WebURL(result.link).to_markdown()))

        results = await asyncio.gather(*tasks)

        output: list[DetailedSearchResult] = []
        for search_result, detail in zip(search_results, results):
            output.append(
                DetailedSearchResult(
                    title=search_result.title,
                    link=search_result.link,
                    snippet=search_result.snippet,
                    detail=detail,
                )
            )

        return output
