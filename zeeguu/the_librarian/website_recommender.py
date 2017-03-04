

# returns only HTTP domains. in this way we filter
# out empty domains, and others like the android:
# that we use for internal tracking...
# Returns: list of tuples (domain, date)
def recent_domains_with_times(user):
    domains = []
    domains_and_times = []
    for b in user.bookmarks_chronologically():
        if not b.text.url.domain_name() in domains and 'http' in b.text.url.domain_name():
                domains_and_times.append([b.text.url.domain_name(), b.time])
                domains.append(b.text.url.domain_name())
    return domains_and_times


def frequent_domains(user):
    domains = map (lambda b: b.text.url.domain_name(), user.bookmarks_chronologically())
    from collections import Counter
    counter = Counter(domains)
    return counter.most_common()


def recommended_urls(user):
    urls_to_words = {}
    for bookmark in user.all_bookmarks():
        if bookmark.text.url.url != "undefined":
            urls_to_words.setdefault(bookmark.text.url,0)
            urls_to_words [bookmark.text.url] += bookmark.origin.importance_level()
    return sorted(urls_to_words, key=urls_to_words.get, reverse=True)


#     Reading recommendations
def recommendations(user):
    recommendations = {
        'de': [
                ['Der Spiegel', 'http://m.spiegel.de', 'German News']
        ],
        'da': [
            ['DR Forsiden', 'http://www.dr.dk', 'Danish News']
        ],
        'nl': [
            ['Het laatste nieuws', 'http://www.nu.nl/', 'Dutch News']
        ],
        'fr': [
            ['Le Figaro', 'http://www.lefigaro.fr/', 'French News']
        ],
        'gr': [
            ['News 247', 'http://news247.gr/', 'Greek News']
        ],
        'it': [
            ['la Reppublica', 'http://www.repubblica.it/', 'Italian News']
        ],
        'no': [
            ['Dagbladet', 'http://www.nrk.no/', 'Norwegian News']
        ],
        'pt': [
            ['Jornal de Noticias', 'http://www.jn.pt/paginainicial/', 'Portughese News']
        ],
        'ro': [
            ['Mediafax', 'http://www.mediafax.ro/', 'Romanian News']
        ],
        'es': [
            ['El Pais', 'http://elpais.com/', 'Spanish News']
        ]
    }

    try:
        return recommendations[user.learned_language_id]
    except:
        return []