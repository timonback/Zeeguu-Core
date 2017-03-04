import json

import zeeguu
import xml.etree.ElementTree


# The demo of the API is available at
#
#     https://api.collinsdictionary.com/apidemo/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # #


def get_all_possible_translations_from_the_collins_api(word):
    """

    :param word: a string

    :return: a triple with:
        1. a list of translations
        2. the full text entry of the translation in XML and
        3. HTML
    """

    from zeeguu.translation.libs.collins_api import API

    api = API(baseUrl="https://api.collinsdictionary.com"+'/api/v1/',
              accessKey=zeeguu.app.config.get("COLLINS_API_KEY"))

    xml_data = json.loads(api.searchFirst("german-english", word, "xml"), "utf-8")

    e = xml.etree.ElementTree.fromstring(xml_data["entryContent"].encode('utf-8'))

    return extract_translations_from_collins_entry(e)


def extract_translations_from_collins_entry(element_tree):
    """

        Fish for the translations in the xml

    :param element_tree:

    :return: List with strings representing translations

    """
    results = []

    translation_xpath =".//sense[@n]/cit[@type='translation']/quote"
    #
    # XPath Syntax
    # . current element
    # // all subelements on all levels below the current one
    # See: https://docs.python.org/2/library/xml.etree.elementtree.html#xpath-support

    for translation_node in element_tree.findall(translation_xpath):
        try:
            results.append(translation_node.text)
        except:
            pass

    return set(results)
