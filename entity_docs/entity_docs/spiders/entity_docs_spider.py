import scrapy

from entity_docs.items import EntityDocsItem

from unidecode import unidecode


def ascii_convert(phrase):
    # Repeated from phrases to avoid circular dependency
    if isinstance(phrase, unicode):
        return unidecode(phrase).strip()
    else:
        return phrase.strip()

def get_urls():
    urls = []
    with open('clean_urls.csv', 'rU') as f:
        for line in f.readlines():
            cells = line.split(',')
            url = ascii_convert(cells[-1])
            urls.append(url)
    return urls

def get_domains(urls):
    new_urls = []
    for url in urls:
        try:
            domain = url.split('//')[1]
            domain = domain.split('/')[0]
            new_urls.append(domain)
        except:
            pass
    return new_urls


class EntityDocsSpider(scrapy.Spider):
    name = "entity_docs"
    urls = get_urls()[100:130]
    print get_domains(urls)
    allowed_domains = get_domains(urls)
    start_urls = urls

    def parse(self, response):
        links = response.xpath('//a/@href').extract()
        for link in links:
            url = response.urljoin(link)
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
