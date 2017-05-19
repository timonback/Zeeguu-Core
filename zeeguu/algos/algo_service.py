import traceback
import zeeguu

from zeeguu.model import Bookmark, BookmarkPriorityARTS, ExerciseSource, Exercise

from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper
from zeeguu.algos.analysis.normal_distribution import NormalDistribution
from zeeguu.algos.arts.arts_rt import ArtsRT

from zeeguu.model.learner_stats.exercise_stats import ExerciseStats

db = zeeguu.db


class AlgoService:
    algorithm_wrapper = AlgorithmWrapper(ArtsRT())
    MAX_PRIORITY = 1000

    @classmethod
    def update_exercise_source_stats(cls):
        exercise_sources = list(ExerciseSource.query.all())
        for source in exercise_sources:
            exercises = Exercise.query.filter_by(source_id=source.id)
            reaction_times = map(lambda x: x.solving_speed, exercises)
            mean, sd = NormalDistribution.calc_normal_distribution(reaction_times)
            exercise_stats = ExerciseStats(source, mean, sd)
            db.session.merge(exercise_stats)

        db.session.commit()

    @classmethod
    def update_bookmark_priority(cls, db, user):
        try:
            bookmarks_for_user = Bookmark.find_by_specific_user(user)
            # tuple(0=bookmark, 1=exercise)
            bookmark_exercise_of_user = map(cls._get_exercise_of_bookmarks, bookmarks_for_user)
            max_iterations = max(pair[1].id for pair in bookmark_exercise_of_user)
            exercises_and_priorities = map(
                (lambda x: (
                    x[0],
                    cls.algorithm_wrapper.calculate(x[1], max_iterations))
                # in case the item has not been studied before
                if x[1] is not None else cls.MAX_PRIORITY
                 )
                , bookmark_exercise_of_user)

            with db.session.no_autoflush:
                for pair in exercises_and_priorities:
                    bpa = BookmarkPriorityARTS(pair[0], pair[1])
                    db.session.merge(bpa)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Error during updating bookmark priority')
            print e.message
            print(traceback.format_exc())

    @staticmethod
    def _get_exercise_of_bookmarks(bookmark):
        if 0 < len(bookmark.exercise_log):
            return bookmark, bookmark.exercise_log[-1]

        return bookmark, None
