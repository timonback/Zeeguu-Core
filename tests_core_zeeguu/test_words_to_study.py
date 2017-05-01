from datetime import datetime

import zeeguu
from model_test_mixin import ModelTestMixIn
from unittest import TestCase

from zeeguu.model import Exercise, ExerciseOutcome, ExerciseSource


class WordsToStudyTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super(WordsToStudyTest, self).setUp()

    def test_bookmarks_to_study(self):
        """
            
            Make sure that once an exercise has been done, it is not
            recommended for study again
              
        """
        original_bookmarks_to_study = self.mir.bookmarks_to_study()
        first_bookmark_to_study = original_bookmarks_to_study[0]

        # solve one exercise
        correct = ExerciseOutcome(ExerciseOutcome.CORRECT)
        recognize = ExerciseSource("Recognize")
        exercise = Exercise(correct, recognize, 100, datetime.now())
        first_bookmark_to_study.exercise_log.append(exercise)

        # save the thing to the db
        zeeguu.db.session.add(exercise)
        zeeguu.db.session.commit()

        # now let's get a new recommendation and make sure that the
        # exercise we just did is not in there again
        bookmarks_to_study = self.mir.bookmarks_to_study()

        assert first_bookmark_to_study not in bookmarks_to_study








