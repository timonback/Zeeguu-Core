
import threading
import time
from zeeguu.content_retriever.content_extractor import ArticleContentExtractor
import queue


def get_content_for_urls(urls, lang_code, timeout = 10):
    """
    :param data: an array of tuples (url, url_id)
    :param lang_code: str
    :param timeout: seconds to wait for the contents
    :return:
    """

    art_queue = queue.Queue()

    # Start worker threads to get url contents
    threads = []
    for url in urls:
        thread = threading.Thread(target=ArticleContentExtractor.worker, args=(url, lang_code, art_queue))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Wait for workers to finish until timeout
    stop = time.time() + timeout
    while any(t.isAlive() for t in threads) and time.time() < stop:
        time.sleep(0.1)

    content_list = []
    for i in range(len(urls)):
        try:
            content_list.append(art_queue.get_nowait())
        except queue.Empty:
            pass

    return content_list
