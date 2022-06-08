from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from numpy import nan
from bs4 import BeautifulSoup
from lxml import etree
import requests

# busqueda = input("¿Qué artículo deseas buscar en Hiraoka?: ")

class HiraokaSpider(CrawlSpider):
    name = 'hiraoka'
    allowed_domains = ['hiraoka.com.pe']
    #start_urls = ['https://hiraoka.com.pe/computo-y-tecnologia/computadoras/{}'.format(busqueda)]
    start_urls = ['https://hiraoka.com.pe/computo-y-tecnologia/computadoras/laptops']
    #start_urls = ['https://hiraoka.com.pe/computo-y-tecnologia/computadoras/laptops/laptop-asus-ux371ea-hl711w-13-3-intel-core-i7-1165g7-1tb-ssd-16gb-ram']

    rules = (
        Rule(LinkExtractor(allow='p='), follow=True),
        Rule(LinkExtractor(allow='computo-y-tecnologia/computadoras/laptops/laptop-'), callback='parse_filter', follow=True),
    )

    def parse_filter(self, response):
        
        titulo = response.xpath("//div[@class='page-title-wrapper product']/h1/span/text()").get()
        link = response.xpath("//link[@rel='canonical']/@href").get()
        marca = response.xpath("normalize-space(//h5[@class='product brand product-item-brand']/text())").get()

        precio = response.xpath("//span[@class='price']/text()").getall()
        precio_limpio = []
        for i in precio:
            i = i.replace('S/ ', '')
            precio_limpio.append(i)

        precio_online = min(precio_limpio)
        precio_normal = max(precio_limpio)

        link_imagen =response.xpath("//div[@class='gallery-placeholder _block-content-loading']/img/@src").get()
        cant_disponible = response.xpath("//div[@class='box-tocart hiraoka-controls']/h3/text()").get()

        atributos = response.xpath("//div[@class='xpec-tab hiraoka-product-details-datasheet cambio-prueba']/div/table/tbody/tr/td[1]/text()").getall()
        detalles = response.xpath("//div[@class='xpec-tab hiraoka-product-details-datasheet cambio-prueba']/div/table/tbody/tr/td[2]/text()").getall()
        if atributos[0] == ' Precio':
            atributos.pop(0)
        
        #estado = response.xpath("//div[@class='ui-pdp-header']/div/span/text()").get()
        #estado = estado.split(" ")[0]

        #puntuacion = response.xpath("//p[@class='ui-review-view__rating__summary__average']/text()").get()
        # puntuacion = response.css(".ui-review-view__rating__summary__average::text").extract()
        #ubicacion = response.xpath("//div[@class='ui-seller-info__status-info']/div/p[2]/text()").get()

        #comentarios = response.css(".ui-pdp-questions__questions-list__question::text").getall()
        #comentarios = {"{}".format(i):j for i,j in enumerate(comentarios)}

        yield {
            'Titulo': titulo,
            'Link': link,
            'Link_img': link_imagen,
            'Marca': marca,
            'Precio_Online': precio_online,
            'Precio_Normal': precio_normal,
            'Cant_disponible': cant_disponible,
            'Atributos':atributos,
            'Detalles': detalles,
            #'Estado': estado,
            #'Puntuación': puntuacion,            
            #'Ubicación': ubicacion,
            #'Comentarios': comentarios,
            }