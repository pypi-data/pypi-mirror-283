import asyncio
import logging
from tempfile import TemporaryDirectory

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
            with TemporaryDirectory() as tempdir:
                temp_path = f"{tempdir}/result.md"

                proc = await asyncio.subprocess.create_subprocess_shell(
                    cmd=f"""npx percollate md {self.sanitized_url} --output={temp_path}""",
                    stderr=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    start_new_session=True,
                )

                stdout, stderr = await proc.communicate()

                with open(temp_path, "r+") as f:
                    result = f.read()

                return result
        except Exception as e:
            logger.error(e)
