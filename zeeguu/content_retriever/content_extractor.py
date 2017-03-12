import requests
from readability import Document


class ContentExtractorFromUrl:

    def __init__(self, url):
        response = requests.get(url)
        html = response.text
        self.article = Document(html)

    def get_content(self):
        return self.article.summary()

    @classmethod
    def worker(cls, url, result):
        article = cls(url)
        result.put(dict(content=article.get_content(), image="", url=url))