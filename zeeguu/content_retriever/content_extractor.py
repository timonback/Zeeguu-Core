import watchmen


class ArticleContentExtractor:
    """
    
        Get the text of the given article
        
    """

    def __init__(self, url, lang_code):
        self.url = url

    @classmethod
    def worker(cls, url, lang_code, result):
        print ("Worker getting the content for " + url)
        article = watchmen.article_parser.get_article(url)
        print("SUCCESS: worker got content for " + url)
        result.put(dict(content=article.text, image="", url=url))
