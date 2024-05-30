import scrapy

from src.processors.comments import CommentsProcessor
from src.processors.gebiet_list import GebietListProcessor
from src.processors.gebiet import GebietProcessor
from src.processors.gipfel import GipfelProcessor
from src.processors.wege_list import WegeListProcessor


class TeufelsturmSpider(scrapy.Spider):
    name = "teufelsturm"

    start_urls = [
        "https://www.teufelsturm.de/gebiete"
    ]

    def __init__(self):
        super().__init__()
        comments_processor = CommentsProcessor()
        gipfel_processor = GipfelProcessor()
        wege_list_processor = WegeListProcessor(comments_processor)
        gebiet_processor = GebietProcessor(gipfel_processor, wege_list_processor)
        self.gebiet_list_processor = GebietListProcessor(gebiet_processor)

    def parse(self, response, **kwargs):
        yield from self.gebiet_list_processor.process(response)
