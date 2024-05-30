from pathlib import Path


class CommentsProcessor:
    def process(self, response):
        self._write_comments_html(response.url, response.body)

    @staticmethod
    def _write_comments_html(url: str, body: bytes):
        number = url.split("=")[-1]
        filename = f"output/comments/{number}.html"
        Path(filename).write_bytes(body)
