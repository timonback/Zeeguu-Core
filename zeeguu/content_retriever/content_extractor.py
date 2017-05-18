from newspaper import Article


class ArticleContentExtractor:
    """
    
        Get the text of the given article
        
    """

    def __init__(self, url, lang_code):
        self.article = Article(url=url, language=lang_code)
        self.article.download()
        self.article.parse()

    def get_content(self):
        return self.article.text

    @classmethod
    def worker(cls, url, lang_code, result):
        extractor = cls(url, lang_code)
        result.put(dict(content=extractor.get_content(), image="", url=url))
