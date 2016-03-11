import scrapy

from entity_docs.items import EntityDocsItem

from unidecode import unidecode
import urllib


def ascii_convert(phrase):
    # Repeated from phrases to avoid circular dependency
    if isinstance(phrase, unicode):
        return unidecode(phrase).strip()
    else:
        return phrase.strip()

def get_urls():
    ids = []
    urls = []
    with open('clean_urls.csv', 'rU') as f:
        for line in f.readlines():
            cells = line.split(',')
            id = cells[0]
            ids.append(id)
            url = ascii_convert(cells[-1])
            urls.append(url)
    return ids[100:130], urls[100:130]

def extract_domain(url):
    try:
        domain = url.split('//')[1]
        domain = domain.split('/')[0]
        return domain
    except:
        return url


class EntityDocsSpider(scrapy.Spider):
    name = "entity_docs"
    ids, urls = get_urls()
    domains = map(extract_domain, urls)
    allowed_domains = domains
    start_urls = urls
    id_lookup = dict(zip(domains, ids))

    def parse(self, response):
        links = response.xpath('//a/@href').extract()
        for link in links:
            url = response.urljoin(link)
            if url.split('.')[-1] == 'pdf':
                yield scrapy.Request(url, callback=self.parse_pdf)
            else:
                yield scrapy.Request(url, callback=self.parse)

    def parse_pdf(self, response):
        domain = extract_domain(response.url).split("www.")[-1]
        filename = response.url.split('/')[-1]
        item = EntityDocsItem()

        item['entity_id'] = self.id_lookup[domain]
        item['filename'] = urllib.unquote(filename).decode('utf8')
        item['file'] = response.body
        yield item
