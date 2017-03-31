# -*- coding: utf-8 -*-

import os


os.environ["CONFIG_FILE"]= os.path.expanduser('~/.config/zeeguu/full_db_test.cfg')
from unittest import TestCase
from model_test_mixin import ModelTestMixIn

from zeeguu.model import SimpleKnowledgeEstimator
from datetime import datetime

from zeeguu.model import Bookmark,  Text, UserWord, Url


class LanguageTest(ModelTestMixIn, TestCase):

    def setUp(self):
        self.no_need_for_db = True
        super(LanguageTest, self).setUp()

    def test_bookmarks_by_date(self):

        bookmarks_list, dates = self.mir.bookmarks_by_date()
        print len(bookmarks_list)

        urls_by_date = {}
        bookmarks_by_url = {}
        for date in dates:
            for bookmark in bookmarks_list[date]:
                urls_by_date.setdefault(date, set()).add(bookmark.text.url)
                bookmarks_by_url.setdefault(bookmark.text.url, []).append(bookmark)

        bookmark_counts_by_date = self.mir.bookmark_counts_by_date()

        for date in dates[0:31]:
            print date.strftime("%A %B %d, %Y")
            for url in urls_by_date.get(date):
                print url.as_string
                for bookmark in bookmarks_by_url.get(url):
                    if bookmark.time.day == date.day:
                        print (bookmark.text.shorten_word_context(bookmark.origin.word, 42))

    def test_knowledge_estimation(self):
        estimator = SimpleKnowledgeEstimator(self.mir, self.mir.learned_language_id)
        data = self.mir.learner_stats_data()

    def test_calculate_probabilities(self):
        text1 = u'Die großen Leute rieten mir dann, das Zeichnen von offenen oder geschlossenen Boas bleiben zu lassen und mich mehr mit Geographie, Geschichte, Mathematik und Grammatik zu beschäftigen. So kam es, dass ich im Alter von sechs eine wunderbare Karriere als Maler aufgab. Ich hatte durch das Scheitern meiner Zeichnungen Nummero 1 und Nummero 2 meinen ganzen Mut verloren. Die großen Leute verstehen nie etwas von selbst. Und für die Kinder ist es viel zu mühevoll, ihnen die Dinge immer und immer wieder von neuem zu erklären'
        text2 = u"Ich zeichnete also das Innere der Boa, damit es die großen Leute genau erkannten, denn sie brauchen immer Erklärungen"

        for i in xrange(15):
            origin = UserWord.find("damit",self.de)
            translation = UserWord.find("therefore", self.en)
            url = Url("http://something.is", "Something Is")
            text = Text(text1, self.de, url)
            bookmark = Bookmark(origin, translation, self.mir, text, datetime.now())
            bookmark.update_encounter_stats_after_adding_a_bookmark(self.mir, bookmark.origin.language)

        for i in xrange(15):
            origin = UserWord.find("damit",self.de)
            translation = UserWord.find("therefore", self.en)
            url = Url("http://something.is/not", "Something Is")
            text = Text(text2, self.de, url)
            bookmark = Bookmark(origin, translation, self.mir, text, datetime.now())
            bookmark.update_encounter_stats_after_adding_a_bookmark(self.mir, bookmark.origin.language)

