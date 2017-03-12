import Queue
import threading

import time
from zeeguu.content_retriever.content_extractor import ContentExtractorFromUrl


def get_content_for_urls(urls, timeout = 10):
    """
    :param data: an array of tuples (url, url_id)
    :param timeout: seconds to wait for the contents
    :return:
    """
    queue = Queue.Queue()

    # Start worker threads to get url contents
    threads = []
    for url in urls:
        thread = threading.Thread(target=ContentExtractorFromUrl.worker, args=(url, queue))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Wait for workers to finish until timeout
    stop = time.time() + timeout
    while any(t.isAlive() for t in threads) and time.time() < stop:
        time.sleep(0.1)

    content_list = []
    for i in xrange(len(urls)):
        try:
            content_list.append(queue.get_nowait())
        except Queue.Empty:
            pass

    return content_list
