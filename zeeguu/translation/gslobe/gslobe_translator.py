# API to retrieve translations from gslobe.com

import json
import urllib2
import urllib


def get_translations_from_gslobe(word, from_language, to_language):

    translations = []

    request = "https://glosbe.com/gapi/translate?" \
              "from="+ from_language +\
              "&dest="+to_language +\
              "&format=json" \
              "&phrase="+ urllib.quote_plus(word.encode('utf8')) +\
              "&pretty=true"
    print (request)
    result = urllib2.urlopen(request).read()

    return extract_translations_from_gslobe_response(result, translations)


def extract_translations_from_gslobe_response(result, translations):
    """
    The output of gslobe is an impressive mess.
     This function tries to make some sense of that

    :param result:
    :param translations:
    :return:
    """
    result_dict = json.loads(result)

    for d in result_dict["tuc"]:
        # the elements of tuc can be
        # "meanings"
        # "meaningId"
        # "authors"
        # "phrase"

        try:
            if d["phrase"]:
                translations.append(d["phrase"]["text"])
        except:
            pass
    return translations
