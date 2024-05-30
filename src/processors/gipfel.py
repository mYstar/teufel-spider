from pathlib import Path


class GipfelProcessor:
    def process(self, response):
        self._write_gipfel_html(response.url, response.body)

    @staticmethod
    def _write_gipfel_html(url: str, body: bytes):
        number = url.split("=")[-1]
        filename = f"output/gipfel/{number}.html"
        Path(filename).write_bytes(body)