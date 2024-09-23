# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

from embedders import insert_doc


class ArticleCrawlerPipeline:
    def process_item(self, item, spider):
        # construct filename
        slug = item["title"].lower()
        slug = re.findall(r"\w+", slug)
        slug = "-".join(slug)
        # construct content
        content = [
            "---",
            f"title: {item['title']}",
            f"author: {item['authors']}",
            f"publish_date: {item['publish_date']}",
            "---",
            item["content"],
        ]
        content = "\n".join(content)

        metadata = {
            "title": item["title"],
            "authors": item["authors"],
            "publish_date": str(item["publish_date"]),
        }
        insert_doc(
            article={
                "content": content,
                "metadata": metadata,
                "slug": slug,
            }
        )

        return item
