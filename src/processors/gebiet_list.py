from pathlib import Path

import scrapy

from src.processors.gebiet import GebietProcessor


class GebietListProcessor:

    def __init__(self, gebiet_processor: GebietProcessor):
        self.gebiet_processor = gebiet_processor

    def process(self, response):
        filename = f"output/index.html"
        Path(filename).write_bytes(response.body)

        all_gebiete = response.xpath("//a/@href[starts-with(., '/gipfel/suche.php?gebietnr=')]").getall()

        for gebiet in all_gebiete:
            url = response.urljoin(gebiet)
            yield scrapy.FormRequest(
                url,
                formdata={"anzahl": "Alle"},
                callback=self.gebiet_processor.process
            )
