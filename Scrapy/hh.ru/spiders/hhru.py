import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru'] #только разрешенные домены, если попадется ссылка на сторонний ресурс - она будет проигнорирована
    start_urls = ['https://hh.ru/search/vacancy?area=2035&area=2025&professional_role=10&professional_role=12&professional_role=25&professional_role=34&professional_role=36&professional_role=73&professional_role=96&professional_role=104&professional_role=107&professional_role=112&professional_role=113&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126&search_field=description&search_field=company_name&search_field=name&text=&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)


    def parse_vacancy(self, response:HtmlResponse):
        name = response.css("h1::text").get()
        salary = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
