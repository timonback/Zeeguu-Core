from datetime import datetime

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from unittest import TestCase

from zeeguu.algos.algo_service import AlgoService
from zeeguu.model import Exercise, ExerciseOutcome, ExerciseSource


class WordsToStudyTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super(WordsToStudyTest, self).setUp()

    def test_bookmarks_to_study(self):
        """
            
            Make sure that once an exercise has been done, it is not
            recommended for study again
              
        """
        AlgoService.update_bookmark_priority(zeeguu.db, self.mir)

        original_bookmarks_to_study = self.mir.bookmarks_to_study()
        first_bookmark_to_study = original_bookmarks_to_study[0]

        # solve one exercise
        correct = ExerciseOutcome(ExerciseOutcome.CORRECT, True)
        recognize = ExerciseSource("Recognize")
        exercise = Exercise(correct, recognize, 100, datetime.now())
        first_bookmark_to_study.exercise_log.append(exercise)

        # save the thing to the db
        zeeguu.db.session.add(exercise)
        zeeguu.db.session.commit()

        AlgoService.update_bookmark_priority(zeeguu.db, self.mir)

        # now let's get a new recommendation and make sure that the
        # exercise we just did is not in there again
        bookmarks_to_study = self.mir.bookmarks_to_study()

        assert first_bookmark_to_study != bookmarks_to_study[0]

    def test_possible_to_have_nothing_to_study(self):
        """

            Once all the bookmarks have been studied
            we don't have anything else

        """
        bookmarks_to_study = self.mir.bookmarks_to_study()

        # solve one exercise
        for bookmark in bookmarks_to_study:
            correct = ExerciseOutcome(ExerciseOutcome.CORRECT)
            recognize = ExerciseSource("Recognize")
            exercise = Exercise(correct, recognize, 100, datetime.now())
            bookmark.exercise_log.append(exercise)

            # save the thing to the db
            zeeguu.db.session.add(exercise)
        zeeguu.db.session.commit()

        # now let's get a new recommendation and make sure that the
        # exercise we just did is not in there again

        # although...
        #     there is currently a temporary trick which
        #     would recommend generic words so we assert
        #     that we *have* what to study
        assert bookmarks_to_study






