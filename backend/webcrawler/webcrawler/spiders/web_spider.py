import scrapy

class WebSpider(scrapy.Spider):
    name = "web_spider"

    start_urls = [
        "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/principles-asset-allocation",
        "https://www.juliusbaer.com/en/insights/wealth-insights/how-to-invest/the-six-basics-of-asset-allocation/"
    ]

    def parse(self, response):

        # extract all para  graph text
        paragraphs = response.css("p::text").getall()

        for p in paragraphs:
            yield {
                "text": p
            }