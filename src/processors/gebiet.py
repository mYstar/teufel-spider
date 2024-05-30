from pathlib import Path

import scrapy

from src.processors.gipfel import GipfelProcessor
from src.processors.wege_list import WegeListProcessor


class GebietProcessor:

    def __init__(self, gipfel_processor: GipfelProcessor, wege_list_processor: WegeListProcessor):
        self.gipfel_processor = gipfel_processor
        self.wege_list_processor = wege_list_processor

    def process(self, response):
        self._write_gebiet_html(response.url, response.body)

        all_gipfel = response.xpath("//a/@href[starts-with(., '/gipfel/details.php?gipfelnr=')]").getall()
        for gipfel in all_gipfel:
            url = response.urljoin(gipfel)
            yield scrapy.Request(
                url,
                callback=self.gipfel_processor.process
            )

        all_wege_lists = response.xpath("//a/@href[starts-with(., '/wege/suche.php?gipfelnr=')]").getall()
        for wege_list in all_wege_lists:
            url = response.urljoin(wege_list)
            yield scrapy.Request(
                url,
                callback=self.wege_list_processor.process
            )

    @staticmethod
    def _write_gebiet_html(url: str, body: bytes):
        number = url.split("=")[-1]
        filename = f"output/gebiet/{number}.html"
        Path(filename).write_bytes(body)
