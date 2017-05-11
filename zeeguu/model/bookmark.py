import re

from sqlalchemy import Column, Table, ForeignKey, Integer
from sqlalchemy.orm import relationship

import zeeguu
from wordstats import Word
from zeeguu.model.ranked_word import WordForm

db = zeeguu.db

from zeeguu.model.exercise_source import ExerciseSource
from zeeguu.model.exercise import Exercise

from zeeguu.model.exercise_outcome import ExerciseOutcome
from zeeguu.model.user_word import UserWord
from datetime import datetime


bookmark_translation_mapping = Table('bookmark_translation_mapping', db.Model.metadata,
    Column('bookmark_id', Integer, ForeignKey('bookmark.id')),
    Column('translation_id', Integer, ForeignKey('user_word.id'))
)

bookmark_exercise_mapping = Table('bookmark_exercise_mapping', db.Model.metadata,
    Column('bookmark_id', Integer, ForeignKey('bookmark.id')),
    Column('exercise_id', Integer, ForeignKey('exercise.id'))
)

WordAlias = db.aliased(UserWord, name="translated_word")


class Bookmark(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.Integer, db.ForeignKey('user_word.id'))
    origin = db.relationship("UserWord", primaryjoin=origin_id == UserWord.id,
                             backref="translations")
    translations_list = relationship("UserWord", secondary="bookmark_translation_mapping")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="bookmarks")

    text_id = db.Column(db.Integer, db.ForeignKey('text.id'))
    text = db.relationship("Text", backref="bookmarks")

    time = db.Column(db.DateTime)

    exercise_log = relationship("Exercise", secondary="bookmark_exercise_mapping")

    def __init__(self, origin, translation, user, text, time):
        self.origin = origin
        self.translations_list.append(translation)
        self.user = user
        self.time = time
        self.text = text

    def __repr__(self):
        # TODO: make the encoding to he utf-8 and change the
        # log file on the server accordingly!
        return u"Bookmark[{3} of {4}: {0}->{1} in '{2}...']\n".\
            format(self.origin.word, self.translation().word, self.text.content[0:10], self.id, self.user_id).\
            encode('ascii', 'ignore')

    def add_new_exercise(self, exercise):
        self.exercise_log.append(exercise)

    def translation(self):
        return self.translations_list[0]

    def translations_rendered_as_text(self):
        return ", ".join(self.translation_words_list())

    def translation_words_list(self):
        translation_words=[]
        for translation in self.translations_list:
            translation_words.append(translation.word)
        return translation_words

    def add_new_translation(self, translation):
        self.translations_list.append(translation)

    def context_is_not_too_long(self):
        return len(self.text.content) < 60

    def events_prevent_further_study(self):
        from zeeguu.model.smartwatch.watch_interaction_event import WatchInteractionEvent
        events_for_self = WatchInteractionEvent.events_for_bookmark(self)
        return any([x.prevents_further_study() for x in events_for_self])

    def good_for_study(self):
        # ML TODO: Must replace call to check_is_latest_outcome... with has_been_learned!
        return not self.check_is_latest_outcome_too_easy() and not self.events_prevent_further_study()

    def remove_translation(self,translation):
        if translation in self.translations_list:
            self.translations_list.remove(translation)

    def add_exercise_outcome(self, exercise_source, exercise_outcome, exercise_solving_speed):
        new_source = ExerciseSource.query.filter_by(
        source = exercise_source
    ).first()
        new_outcome=ExerciseOutcome.query.filter_by(
        outcome=exercise_outcome
    ).first()
        exercise = Exercise(new_outcome,new_source,exercise_solving_speed, datetime.now())
        self.add_new_exercise(exercise)
        db.session.add(exercise)

    def split_words_from_context(self):

        result = []
        bookmark_content_words = re.findall(r'(?u)\w+', self.text.content)
        for word in bookmark_content_words:
            if word.lower() != self.origin.word.lower():
                result.append(word)

        return result

    def json_serializable_dict(self, with_context=True):
        result = dict(
                    id=self.id,
                    to=self.translation_words_list(),
                    from_lang=self.origin.language_id,
                    to_lang=self.translation().language.id,
                    title=self.text.url.title,
                    url=self.text.url.as_string(),
                    origin_importance=Word.stats(self.origin.word, self.origin.language_id).importance
                )
        result["from"] = self.origin.word
        if with_context:
            result['context'] = self.text.content
        return result


    @classmethod
    def find_by_specific_user(cls, user):
        return cls.query.filter_by(
            user= user
        ).all()

    @classmethod
    def find_all(cls):
        return cls.query.filter().all()

    @classmethod
    def find_all_for_text(cls,text):
        return cls.query.filter(cls.text == text).all()

    @classmethod
    def find(cls, b_id):
        return cls.query.filter_by(
            id= b_id
        ).first()

    @classmethod
    def find_all_by_user_and_word(cls, user, word):
        return cls.query.filter_by(
            user = user,
            origin = word
        ).all()

    @classmethod
    def find_all_by_user_word_and_text(cls, user, word, text):
        return cls.query.filter_by(
            user = user,
            origin = word,
            text = text
        ).all()

    def check_is_latest_outcome_too_easy(self, add_to_result_time=False):
        sorted_exercise_log_by_latest=sorted(self.exercise_log, key=lambda x: x.time, reverse=True)
        for exercise in sorted_exercise_log_by_latest:
            if exercise.outcome.outcome == ExerciseOutcome.TOO_EASY:
                if add_to_result_time:
                    return True, exercise.time
                return True
            elif exercise.outcome.outcome == ExerciseOutcome.SHOW_SOLUTION or exercise.outcome.outcome == ExerciseOutcome.WRONG:
                if add_to_result_time:
                    return False, None
                return False
        if add_to_result_time:
            return False, None
        return False

    def already_seen_today(self, add_to_result_time=False):
        sorted_exercise_log_by_latest=sorted(self.exercise_log, key=lambda x: x.time, reverse=True)

        if not sorted_exercise_log_by_latest:
            # no exercise log => clearly not seen today
            return False

        last_seen = sorted_exercise_log_by_latest[0]
        if last_seen.time.date() == datetime.now().date():
            return True

        return False


    def check_if_learned_based_on_exercise_outcomes (self, add_to_result_time=False):
        """
        TODO: This should replace check_is_latest_outcome in the future...

        :param add_to_result_time:
        :return:
        """
        sorted_exercise_log_by_latest=sorted(self.exercise_log, key=lambda x: x.time, reverse=True)

        if sorted_exercise_log_by_latest:
            last_exercise = sorted_exercise_log_by_latest[0]

            # If last outcome is TOO EASY we know it
            if last_exercise.outcome.outcome == ExerciseOutcome.TOO_EASY:
                if add_to_result_time:
                    return True, last_exercise.time
                return True

            CORRECTS_IN_A_ROW = 5
            if len(sorted_exercise_log_by_latest) > CORRECTS_IN_A_ROW:

                # If we got it right for the last CORRECTS_IN_A_ROW times, we know it
                if all(exercise.outcome.outcome == ExerciseOutcome.CORRECT for exercise in sorted_exercise_log_by_latest[0:CORRECTS_IN_A_ROW-1]):
                    return True, last_exercise.time

        if add_to_result_time:
            return False, None
        return False

    def events_indicate_its_learned(self):
        from zeeguu.model.smartwatch.watch_interaction_event import WatchInteractionEvent
        events_for_self = WatchInteractionEvent.events_for_bookmark(self)

        for event in events_for_self:
            if event.is_learned_event():
                return True, event.time

        return False, None

    def has_been_learned(self, also_return_time=False):
        # TODO: This must be stored in the DB together with the
        # bookmark... once a bookmark has been learned, we shoud
        # not ever doubt it ...

        """
        :param also_return_time: should the function return also the time when
        the bookmark has been learned?

        :return: boolean indicating whether the bookmark has already been learned,
        togetgher with the time when it was learned if also_return_time is set
        """

        # The first case is when we have an exercise outcome set to Too EASY
        learned, time = self.check_if_learned_based_on_exercise_outcomes(True)
        if learned:
            if also_return_time:
                return True, time
            else:
                return True

        # The second case is when we have an event in the smartwatch event log
        # that indicates that the word has been learned
        learned, time = self.events_indicate_its_learned()
        if learned:
            return learned, time

        if also_return_time:
            return False, None

        return False

