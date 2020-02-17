# -*- coding: utf-8 -*-

import scrapy


class GpSeSpider(scrapy.Spider):
    name = 'sweclockers.com'
    allowed_domains = ['sweclockers.com']
    start_urls = ['https://www.sweclockers.com']

    def parse(self, response):

        for resp in response.xpath('//div[contains(@class, "itemBody")]/h2/a/@href'):
            yield response.follow(resp.get(), self.parseArticle)

    def parseArticle(self, r):
        text = ""
        for a in r.xpath('//div[contains(@class,"articleContent")]//div[contains(@class,"bbcode")]/p[contains(@class,"bbParagraph")]'):
            text += "".join(a.xpath('.//text()').getall()).strip()
            text += "\n\n"
        yield {
            'date': "" + r.xpath('//ul[contains(@class,"meta")]').xpath('.//li[contains(@class,"date")]/time/@datetime').get(),
            'category': "" + r.xpath('//ul[contains(@class,"meta")]').xpath('.//li[contains(@class,"category")]/a/text()').get(),
            'author': "" + r.xpath('//ul[contains(@class,"meta")]').xpath('.//li[contains(@class,"authors-byline")]//a/text()').get(),
            'header': str(r.xpath('//h1[contains(@itemprop,"headline")]/text()').get()).strip().replace("\t", "").replace("\n\n\n", "\n\n"),
            'preamble': str(r.xpath('//div[contains(@class,"preamble")]//p/text()').get()).strip(),
            'text': text,
            'url': r.url,
        }
