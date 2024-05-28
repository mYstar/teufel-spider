from pathlib import Path

import scrapy

from src.processors.gipfel import GipfelProcessor


class GebietProcessor:

    def __init__(self, gipfel_processor: GipfelProcessor):
        self.gipfel_processor = gipfel_processor

    def process(self, response):
        filename = f"output/index.html"
        Path(filename).write_bytes(response.body)

        alle_gipfel = response.xpath("//a/@href[starts-with(., '/gipfel/suche.php?gebietnr=')]").getall()

        for gipfel in alle_gipfel:
            url = response.urljoin(gipfel)
            yield scrapy.FormRequest(
                url,
                formdata={"anzahl": "Alle"},
                callback=self.gipfel_processor.process
            )

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # response.xpath('//*[text()="Longitude"]/parent::*/following-sibling::*/font/text()').get()
        # response.xpath('//b/font[@size="3"]/text()').get()
        # response.xpath('//b/font[@size="2"]/text()').re('\[(.*)\]')[0]
