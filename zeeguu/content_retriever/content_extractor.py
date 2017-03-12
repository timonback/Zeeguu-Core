import urllib2

import BeautifulSoup
import requests
from goose import Goose
from readability import Document


class ContentExtractorFromUrl:
    goose = Goose()

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

        # BeautifulSoup.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        # response = opener.open(url)
        # raw_html = response.read().decode('utf8')
        # soup = BeautifulSoup(raw_html)
        # paragraphs = soup.findAll('p', {'class': 'story-body-text story-content'})