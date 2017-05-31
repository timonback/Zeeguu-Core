import itertools
import traceback

import zeeguu

from zeeguu.model.bookmark import Bookmark
from zeeguu.model.bookmark_priority_arts import BookmarkPriorityARTS
from zeeguu.model.exercise import Exercise
from zeeguu.model.exercise_source import ExerciseSource

from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper
from zeeguu.algos.analysis.normal_distribution import NormalDistribution
from zeeguu.algos.arts.arts_rt import ArtsRT
from zeeguu.model.learner_stats.exercise_stats import ExerciseStats

db = zeeguu.db


class AlgoService:
    algorithm_wrapper = AlgorithmWrapper(ArtsRT)
    MAX_PRIORITY = 1000

    @classmethod
    def update_exercise_source_stats(cls):
        exercise_sources = list(ExerciseSource.query.all())
        for source in exercise_sources:
            exercises = Exercise.query.filter_by(source_id=source.id)
            reaction_times = map(lambda x: x.solving_speed, exercises)
            mean, sd = NormalDistribution.calc_normal_distribution(
                reaction_times)
            exercise_stats = ExerciseStats(source, mean, sd)
            db.session.merge(exercise_stats)

        db.session.commit()

    @classmethod
    def update_bookmark_priority(cls, db, user):
        try:
            bookmarks_for_user = user.all_bookmarks()
            if len(bookmarks_for_user) == 0:
                return

            # tuple(0=bookmark, 1=exercise)
            bookmark_exercise_of_user = map(cls._get_exercise_of_bookmark, bookmarks_for_user)
            b1, b2 = itertools.tee(bookmark_exercise_of_user, 2)

            max_iterations = max(pair[1].id if pair[1] is not None else 0 for pair in b1)
            exercises_and_priorities = map(lambda x: (x[0], cls.algorithm_wrapper.calculate(x[1], max_iterations) if x[1] else cls.MAX_PRIORITY), b2)

            with db.session.no_autoflush:
                for pair in exercises_and_priorities:
                    entry = BookmarkPriorityARTS.query.filter_by(
                        bookmark_id=pair[0].id)
                    if entry.first() is not None:
                        entry.first().priority = pair[1]
                    else:
                        db.session.add(BookmarkPriorityARTS(pair[0], pair[1]))

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error during updating bookmark priority')
            print(e)
            print(traceback.format_exc())

    @staticmethod
    def _get_exercise_of_bookmark(bookmark):
        if 0 < len(bookmark.exercise_log):
            return bookmark, bookmark.exercise_log[-1]

        return bookmark, None

