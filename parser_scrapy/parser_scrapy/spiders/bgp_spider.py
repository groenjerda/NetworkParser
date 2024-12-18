from typing import Any

import scrapy
from scrapy.http import Response


class BGPSpider(scrapy.Spider):
    name = 'bgp'

    def __init__(self, link, *args, **kwargs):
        super(BGPSpider, self).__init__(*args, **kwargs)
        self.start_urls = (link,)
        # для вызова из скрипта
        # process = CrawlerProcess()
        # process.crawl(MySpider, category="electronics")

    def parse(self, response: Response):
        for row in response.css('[id=table_prefixes4] tbody tr'):
            tds = row.css('td')
            yield {
                'network': tds[0].css('a::text').get(),
                'provider': tds[1].css('::text').get().strip()
            }
