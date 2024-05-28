import scrapy

from src.processors.gebiet import GebietProcessor
from src.processors.gipfel import GipfelProcessor


class TeufelsturmSpider(scrapy.Spider):
    name = "teufelsturm"

    start_urls = [
        "https://www.teufelsturm.de/gebiete"
    ]

    def __init__(self):
        super().__init__()
        self.gipfel_processor = GipfelProcessor()
        self.gebiet_processor = GebietProcessor(self.gipfel_processor)

    # def start_requests(self):
    #     yield scrapy.FormRequest(
    #         url="https://www.teufelsturm.de/gebiete",
    #         formdata={"anzahl": "Alle"},
    #         callback=self.parse
    #     )

    def parse(self, response, **kwargs):
        yield from self.gebiet_processor.process(response)
