import scrapy

from entity_docs.items import EntityDocsItem

def get_urls():
    urls = []
    with open('clean_urls.csv', 'r') as f:
        for line in f.readlines():
            cells = line[-2].split(',')
            url = cells[-1]
            urls.append(url)
    return urls

class EntityDocsSpider(scrapy.Spider):
    name = "entity_docs"
    urls = get_urls()[:1]
    print urls
    allowed_domains = urls
    start_urls = urls
    # allowed_domains = ["aatwp.org"]
    # start_urls = [
    #     "http://aatwp.org/budget-public-hearing-dec-21-at-730-pm/"
    # ]

    def parse(self, response):
        links = response.xpath('//a/@href').extract()
        for link in links:
            url = response.urljoin(link)
            print url
            if url.split('.')[-1] == 'pdf':
                yield scrapy.Request(url, callback=self.parse_pdf)
            else:
                yield scrapy.Request(url, callback=self.parse)

    def parse_pdf(self, response):
        filename = response.url.split('/')[-1]
        item = EntityDocsItem()
        item['filename'] = filename
        item['file'] = response.body
        yield item
