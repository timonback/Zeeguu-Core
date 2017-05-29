from zeeguu.content_retriever.parallel_retriever import get_content_for_urls


def retrieve_urls_and_compute_metrics(urls, language, user, timeout = 10):

    urls_and_metrics = {}
    content_and_urls = get_content_for_urls(urls, language.id, timeout)

    for each in content_and_urls:
        try:
            difficulty = user.text_difficulty(each['content'],language)
            urls_and_metrics[each['url']] = {
                'difficulty': {
                    'normalized':   difficulty['normalized'],
                    'discrete'  :   difficulty['discrete'],
                    'average'   :   difficulty['score_average']
                }
            }
        except Exception as e:
            print ("Failed while trying to compute difficulty for " + each['url'])
            print (str(e))

    return urls_and_metrics
