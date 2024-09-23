import requests
from bs4 import BeautifulSoup
from newspaper import Article
from rich.progress import track
import pandas as pd


def get_article_metadata(article: Article) -> dict:
    authors = ", ".join(article.authors)
    publish_date = article.publish_date
    return {
        "url": article.url,
        "title": article.title,
        "authors": authors,
        "publish_date": publish_date,
        "thumbnail_url": article.top_image,
    }


def main() -> None:
    url = "https://mojok.co/liputan-mojok/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    urls = [a.get("href") for a in soup.select("h3 a")]
    items = []
    for url in track(urls, description="Downloading articles..."):
        article = Article(url=url, language="id")
        article.download()
        article.parse()
        item = get_article_metadata(article)
        item["content"] = article.text
        items.append(item)
    df = pd.DataFrame(items)
    df.to_csv("mojok_articles.csv", index=False)


if __name__ == "__main__":
    main()
