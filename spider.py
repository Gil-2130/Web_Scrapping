import scrapy

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    base_url = 'http://books.toscrape.com/'

    def parse(self, response):
        todos_os_livros = response.xpath('//article[@class="product_pod"]')

        for livro in todos_os_livros:
            liv_url = livro.xpath('.//h3/a/@href').extract_first()

            if 'catalogue/' not in liv_url:
                liv_url = 'catalogue/' + liv_url

            liv_url = self.base_url + liv_url

            yield scrapy.Request(liv_url, callback=self.parse_livro)

        prox_url_parc = response.xpath('//li[@class="next"]/a/@href').extract_first()

        if 'catalogue/' not in prox_url_parc:
            prox_url_parc = 'catalogue/' + prox_url_parc
        
        prox_url_full = self.base_url + prox_url_parc

        yield scrapy.Request(prox_url_full, callback=self.parse)
        
    def parse_livro(self, response):
        titulo = response.xpath('//div/h1/text()').extract_first()
        img_relac = response.xpath('//div[@class="item active"]/img/@src').extract_first()
        img_final = self.base_url + img_relac.replace('../..', '')
        preço = response.xpath(
            '//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').extract_first()
        estoque = response.xpath('//div[contains(@class, "product_main")]/p[contains(@class, "instock availability")]/text()').extract()[1].strip()
        estrelas = response.xpath(
            '//div/p[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating', '')
        descrição_livro = response.xpath(
            '//div[@id="product_description"]/following-sibling::p/text()').extract_first()
        upc = response.xpath(
            '//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
        preço_s_taxa = response.xpath(
            '//table[@class="table table-striped"]/tr[3]/td/text()').extract_first()
        preço_c_taxa = response.xpath(
            '//table[@class="table table-striped"]/tr[4]/td/text()').extract_first()
        taxa = response.xpath(
            '//table[@class="table table-striped"]/tr[5]/td/text()').extract_first()

        yield {
            'Titulo' : titulo,
            'Imagem' : img_relac, 
            'Imagem Final' : img_final,   
            'Preço' : preço,
            'Estoque': estoque,
            'Estrelas': estrelas,
            'Descrição do livro': descrição_livro,
            'Identificador' : upc,
            'Preço sem Taxa' : preço_s_taxa, 
            'Preço com Taxa': preço_c_taxa, 
            'Taxa' :taxa,
        }
