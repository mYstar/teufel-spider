from pathlib import Path

import scrapy

from src.items import ImagesItem


class WegeListProcessor:

    def __init__(self, comments_processor):
        self.comments_processor = comments_processor

    def process(self, response):
        self._write_wege_list_html(response.url, response.body)

        # download the symbol images
        images_item = ImagesItem()
        image_urls = response.xpath('//img[contains(@src, "/img/symbole/")]/@src').extract()
        absolute_urls = [response.urljoin(url) for url in image_urls]
        images_item['image_urls'] = absolute_urls
        yield images_item

        weg_comments = response.xpath("//a/@href[starts-with(., '/wege/bewertungen/anzeige.php?wegnr=')]").getall()
        weg_comments = (url for url in weg_comments)

        for comments in weg_comments:
            url = response.urljoin(comments)
            yield scrapy.Request(
                url,
                callback=self.comments_processor.process
            )

    @staticmethod
    def _write_wege_list_html(url: str, body: bytes):
        number = url.split("=")[-1]
        filename = f"output/wege/{number}.html"
        Path(filename).write_bytes(body)
