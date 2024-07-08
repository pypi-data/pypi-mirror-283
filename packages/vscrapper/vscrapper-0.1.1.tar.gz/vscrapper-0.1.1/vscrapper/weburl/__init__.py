import asyncio
import subprocess
import logging

from vscrapper.utils import Utils

logger = logging.getLogger(__name__)


class WebURL:
    def __init__(self, url: str, utils: Utils = Utils()):
        self.url = url
        self.utils = utils

        self.sanitized_url = self.utils.sanitize_url(url=self.url)

        if not self.sanitized_url:
            raise Exception("Invalid URL")

    async def to_markdown(self) -> str | None:
        logger.info(f"to markdown")

        try:
            raw = await asyncio.create_subprocess_shell(
                cmd=f"""npx percollate md {self.sanitized_url} --output=-""",
                stdout=subprocess.PIPE,
            )
            res = raw.stdout
            if res:
                res = (await res.read()).decode("utf-8")
                with open("./logs/to_markdown.log", "a+") as f:
                    f.write(res)
            return res
        except Exception as e:
            logger.error(e)
