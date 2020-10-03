import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response:HtmlResponse):
        vacancies = response.xpath("//div[@class='_3mfro PlM3e _2JVkc _3LJqf']/a/@href")
        for vacancy in vacancies:
            yield response.follow(vacancy,callback=self.vacancy_parse)

        next_page = response.xpath("//a[@rel='next']//@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        pass

    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']//text()").extract()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']//text()").extract()
        href= response.url
        yield JobparserItem(name=name, salary=salary, href=href)