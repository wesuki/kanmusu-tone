# -*- coding: utf-8 -*-
import scrapy


class KcwikiZhSpider(scrapy.Spider):
    name = "kcwiki-zh"
    allowed_domains = ["zh.kcwiki.moe"]
    custom_settings = {
    #   'CLOSESPIDER_PAGECOUNT' : 5,
      'DOWNLOAD_DELAY' : 1,
    }
    start_urls = (
        'https://zh.kcwiki.moe/wiki/%E8%88%B0%E5%A8%98%E5%9B%BE%E9%89%B4',
    )

    def parse(self, response):
        ## parse all available Kanmusu
        pages = response.xpath('//table//table[descendant::*[text()="艦娘導航總表"]]//table//table//a').css('a::attr(href)').extract()
        for kanmusu_page in pages :
            yield scrapy.Request(
                response.urljoin(kanmusu_page),
                callback=self.parse_kanmusu)

    def parse_kanmusu(self, response) :
        ## example result: '晓型 / 一番舰 / 驱逐舰\n'
        category_text = (response.css('div.tabbertab table.wikitable'))[0].xpath('//td[@colspan="4"]/text()').extract_first()
        
        yield {
          'name' : response.css('.firstHeading::text').extract_first(),
          'texts' : response.xpath('//h3[1]/following::table[1]//td[@lang]/text()').extract(),
          'category-text' : category_text,
        }
