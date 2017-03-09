from goose import Goose


class ContentExtractorFromUrl:
    goose = Goose()

    def __init__(self, url):
        self.article = ContentExtractorFromUrl.goose.extract(url=url)

    def get_content(self):
        return self.article.cleaned_text

    def get_image(self):
        if self.article.top_image is not None:
            return self.article.top_image.src
        else:
            return ""

    @classmethod
    def worker(cls, url, result):
        article = cls(url)
        result.put(dict(content=article.get_content(), image=article.get_image(), url=url))