from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from avitoparser.spiders.avito import AvitoSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    # query = input('')
    runner.crawl(AvitoSpider, query='bmw')

    reactor.run()
