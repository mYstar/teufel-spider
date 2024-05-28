from pathlib import Path


class GipfelProcessor:

    def process(self, response):
        number = response.url.split("=")[-1]
        filename = f"output/gebiet/{number}.html"
        Path(filename).write_bytes(response.body)
