# -*- coding: utf-8 -*-

import scrapy
from datetime import date, timedelta

class GpSeSpider(scrapy.Spider):
    name = 'flashback.org'
    allowed_domains = ['flashback.org']
    start_urls = ['https://www.flashback.org/aktuella-amnen']
    category = ""

    def parse(self, response):

        # 4 categories; news, misc, >1week, >1year
        for resp in response.xpath('//div[contains(@id, "site-left")]/table').xpath('.//a[contains(@class, "thread-title")]'):
            category = "".join(resp.xpath('./../../../../caption/text()').getall()).strip()
            yield response.follow(resp.xpath('./@href').get(), self.parseCategory, meta={'category': category})

    def parseCategory(self, r):
        post = r.xpath('//div[contains(@id, "posts")]/div[1]')

        postdate = "".join(post.xpath('.//div[contains(@class, "post-heading")]/text()').getall()).strip()
        if "Idag" in postdate:
            postdate = postdate.replace("Idag", str(date.today()))
        elif "Igår" in postdate:
            postdate = postdate.replace("Igår", str(date.today() - timedelta(days=1)))

        textdata = ""
        for chunk in post.xpath('.//div[contains(@id, "post_message")]//text()'):
            tmp = chunk.get().strip()
            textdata += chunk.get().strip()
            # For every independent chunk of text, insert a new paragraph.
            if len(tmp) > 0:
                textdata += "\n\n"

        yield {
            'category': r.meta.get('category'),
            'header': "".join(r.xpath('//div[contains(@class, "page-title")]//text()').getall()).strip(),
            'date': postdate,
            'author': "".join(post.xpath('.//div[contains(@class, "post-user")]/div/a/text()').getall()).strip(),
            'joined': post.xpath('.//div[contains(@class, "post-user-info")]/div[1]/text()').get(),
            'posts': str(post.xpath('.//div[contains(@class, "post-user-info")]/div[2]/text()').get()).strip(),
            'text': textdata,
            'url' : r.url,
        }