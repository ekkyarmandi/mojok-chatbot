import scrapy
from newspaper import Article


class MojokCoSpider(scrapy.Spider):
    name = "mojok_co"
    allowed_domains = ["mojok.co"]
    start_urls = ["https://mojok.co/?s=klitih"]

    def parse(self, response):
        links = response.css("h3 a::attr(href)").getall()
        for link in links:
            yield response.follow(url=link, callback=self.parse_article)
        # paginate to next page
        next_page = response.css("div.jeg_pagination a.next::attr(href)").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_article(self, response):
        content = response.meta.get("content", [])
        article = Article(url=response.url, language="id")
        article.download(input_html=response.text)
        article.parse()
        # find next page
        next_page = response.css("div.nav_link a.next::attr(href)").get()
        if next_page:
            # include article.text in response as metadata on response.follow
            content.append(article.text)
            yield response.follow(
                url=next_page, callback=self.parse_article, meta={"content": content}
            )
        else:
            # if has page not found return Value
            content.append(article.text)
            yield {
                "title": article.title,
                "authors": ", ".join(article.authors),
                "publish_date": article.publish_date,
                "content": "\n\n".join(content),
            }
