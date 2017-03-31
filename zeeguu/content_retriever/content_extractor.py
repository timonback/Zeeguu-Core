import requests
from readability.readability import Document


class ContentExtractorFromUrl:

    def __init__(self, url):
        response = requests.get(url)
        html = response.text
        self.document = Document(html)

    def get_content(self):
        return self.document.summary()

    @classmethod
    def worker(cls, url, result):
        extractor = cls(url)
        result.put(dict(content=extractor.get_content(), image="", url=url))