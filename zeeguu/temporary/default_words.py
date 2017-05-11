# This Python file uses the following encoding: utf-8

"""
    When a new anonymous, or even not anonymous user
    is created, it's good to already offer them some
    words to be able to practice.

    This file takes care of this for the moment.

"""
from datetime import datetime

import zeeguu
from zeeguu.model import Bookmark, Language, Text, Url, UserWord

bookmark_data = dict()

lingnaut_nl = 'http://www.linguanaut.com/english_dutch.htm'
bookmark_data['nl'] = [
    ["voorsichtig", "careful", "Wees voorsichtig!", lingnaut_nl],
    ["waar", "where", "Waar woont u?", lingnaut_nl],
    ["begrijp", "understand", "Ik begrijp het niet", lingnaut_nl],
    ["geweldig", "great", "Dat is geweldig!", lingnaut_nl],
    ["zeg", "say", "Hoe zeg je “Please” in het Nederlands?", lingnaut_nl],
    ["slecht", "bad", "Mijn Nederlands is slecht.", lingnaut_nl],
    ["oefenen", "practice", "Ik moet mijn Nederlands oefenen.", lingnaut_nl],
    ["zorgen", "worry", "Maak je geen zorgen", lingnaut_nl],
    ["Haast", "Hurry", "Haast je!", lingnaut_nl],
    ["nodig", "needed", "Ik heb een dokter nodig.", lingnaut_nl],
    ["terug", "back", "Ik ben zo terug.", lingnaut_nl],
    ["hou van", "like", "Ik hou van de Nederlandse taal", lingnaut_nl]
]

lingnaut_de = 'http://www.linguanaut.com/english_german.htm'
bookmark_data['de'] = [
    ["Ahnung", "idea", "Ich habe keine Ahnung.", lingnaut_de],
    ["jederzeit", "anytime", "Du kannst mich jederzeit anrufen", lingnaut_de],
    ["fällig", "due", "	Die Telefonrechnung ist fällig", lingnaut_de],
    ["vermisse", "miss", "	Ich vermisse dich", lingnaut_de],
    ["einladen", "invite", "Ich möchte Dich zum Abendessen einladen.", lingnaut_de],
    ["esse", "eat", "	Ich esse kein Schweinefleisch!", lingnaut_de],
    ["gehen", "to go", "Möchtest Du spazieren gehen?", lingnaut_de],
    ["verheiratet", "married", "Ich bin verheiratet", lingnaut_de],
    ["schön", "beautiful", "Du siehst schön aus!", lingnaut_de],
    ["Abendessen", "dinner", "Ich möchte Dich zum Abendessen einladen.", lingnaut_de],
    ["langweilig", "boring", "Mir ist langweilig", lingnaut_de]
]

lingnaut_de = 'http://www.linguanaut.com/english_spanish.htm'
bookmark_data['es'] = [
    ["Dónde", "where", "¿Dónde Vives?", lingnaut_de],
    ["Sueños", "dreams", "¡Buenas Noches Y Dulces Sueños!", lingnaut_de],
    ["País", "country", "Me Gustaría Visitar Algún Día Tu País", lingnaut_de],
    ["Gustaría", "I'd like to", "Me Gustaría Visitar Algún Día Tu País", lingnaut_de],
    ["Saludos", "greetings", "Dale Saludos A Juan De Mi Parte", lingnaut_de],
    ["Despacio", "slow", "¡Puedes Hablar Más Despacio!", lingnaut_de],
    ["Entiendo", "understand", "¡No Entiendo!", lingnaut_de],
    ["Malo", "bad", "Mi Español Es Malo", lingnaut_de],
    ["Hambre", "hunger", "Tengo Hambre", lingnaut_de],
    ["Mareado", "sick", "Estoy Mareado.", lingnaut_de],
    ["tomar", "drink", "Qué le gustaría tomar?", lingnaut_de]
]


def default_bookmarks(user, language_code):

    bookmarks = []

    try:
        origin_language = Language.find(language_code)
        english = Language.find("en")

        for data_point in bookmark_data[language_code]:
            origin_word = UserWord.find(data_point[0], origin_language)
            translation = UserWord.find(data_point[1], english)
            url = Url.find(data_point[3], "Zeeguu Exercises")
            text = Text.find_or_create(data_point[2], origin_language, url)

            # we don't create a new bookmark if the user already had it before
            if not Bookmark.find_all_by_user_word_and_text(user, origin_word, text):
                b = Bookmark(origin_word, translation, user, text, datetime.now())
                bookmarks.append(b)
    except Exception as e:
        zeeguu.log("could not load default bookmarks for {0}".format(language_code))

    return bookmarks
