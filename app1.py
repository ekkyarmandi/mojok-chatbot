from newspaper import Article


def get_article_as_markdown(article: Article) -> None:
    authors = ", ".join(article.authors)
    publish_date = article.publish_date.strftime("%Y-%m-%d")
    content = [
        "---",
        f"title: {article.title}",
        f"author: {authors}",
        f"publish_date: {publish_date}",
        f"thumbnail_url: {article.top_image}",
        f"url: {article.url}",
        "---",
        article.text,
    ]
    return "\n".join(content)


def main() -> None:
    url = "https://mojok.co/liputan/seni/lagu-yang-tak-kalah-nyesek-dari-lagu-bernadya/"
    article = Article(url=url, language="id")
    article.download()
    article.parse()
    content = get_article_as_markdown(article)
    with open("article.md", "w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
