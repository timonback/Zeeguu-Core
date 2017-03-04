import json
import zeeguu
from urllib import quote_plus
from urllib2 import urlopen

def translate_using_the_google_API(from_lang_code, to_lang_code, word):
    translate_url = "https://www.googleapis.com/language/translate/v2"
    api_key = zeeguu.app.config.get("TRANSLATE_API_KEY")
    # quote replaces the unicode codes in \x notation with %20 notation.
    # quote_plus replaces spaces with +
    # The Google API prefers quote_plus,
    # This seems to be the (general) convention for info submitted
    # from forms with the GET method
    url = translate_url + \
          "?q=" + quote_plus(word.encode('utf8')) + \
          "&target=" + to_lang_code.encode('utf8') + \
          "&format=text".encode('utf8') + \
          "&source=" + from_lang_code.encode('utf8') + \
          "&key=" + api_key
    result = json.loads(urlopen(url).read())
    translation = result['data']['translations'][0]['translatedText']
    return translation
