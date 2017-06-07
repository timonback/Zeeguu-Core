# -*- coding: utf8 -*-
import datetime
import random

import flask_sqlalchemy
import os

import math
from flask import Flask

import zeeguu

from zeeguu.algos.algo_service import PriorityInfo
from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper
from zeeguu.algos.arts.arts_rt import ArtsRT
from zeeguu.model import User, ExerciseOutcome, Exercise, ExerciseSource


class AverageExercise:

    def __init__(self, exercise_log):
        self.exercise_log = exercise_log
        self.past_exercises = []
        self.priority = 10

        random.seed(0)

        self.avg_solving_speed, self.prob_correct = self._get_avg_exercise(exercise_log)

    @classmethod
    def _get_avg_exercise(cls, exercise_log):
        if len(exercise_log) == 0:
            return 500, 0.5

        avg_speed = cls.__mean([x.solving_speed for x in exercise_log])
        prob_correct = cls.__mean([x.outcome.correct for x in exercise_log])
        return avg_speed, prob_correct

    @staticmethod
    def __mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

    def append_new_exercise(self):
        random_outcome = ExerciseOutcome(ExerciseOutcome.CORRECT) if random.random() < self.prob_correct else ExerciseOutcome(ExerciseOutcome.WRONG)
        new_exercise = Exercise(random_outcome, ExerciseSource("Test"), self.avg_solving_speed, datetime.datetime.now())
        self.past_exercises.append(new_exercise)
        return new_exercise


if __name__ == "__main__":

    zeeguu.app = Flask("Zeeguu-Core-Test")

    config_file = os.path.expanduser('../testing_default.cfg')
    if "CONFIG_FILE" in os.environ:
        config_file = os.environ["CONFIG_FILE"]
    zeeguu.app.config.from_pyfile(config_file,
                                  silent=False)  # config.cfg is in the instance folder

    zeeguu.db = flask_sqlalchemy.SQLAlchemy(zeeguu.app)
    print(("running with DB: " + zeeguu.app.config.get("SQLALCHEMY_DATABASE_URI")))

    zeeguu.db.create_all()


    ###########################################
    ### correct - return after 10
    ### incorrect - return after 3
    user_id = 1
    ArtsRT.w = 1000
    ArtsRT.b
    ArtsRT.r
    ArtsRT.D
    algo_wrapper = AlgorithmWrapper(ArtsRT())

    user = User.find_by_id(user_id)
    bookmarks = user.all_bookmarks()

    print('Using user '+user.name+' with id '+str(user.id))
    print('Found '+str(len(bookmarks))+' bookmarks')

    bookmark_avg_exercise_pairs = [[x, AverageExercise(x.exercise_log)] for x in bookmarks]
    next_bookmark = bookmark_avg_exercise_pairs[0] # to know which exercise to generate next

    for i in range(0, 100):
        new_exercise = next_bookmark[1].append_new_exercise()
        new_exercise.id = i
        print("{:2} - {:} - {:1}".format(i, next_bookmark[0].id, new_exercise.outcome.correct), end=', ')

        max_priority = 0
        for pair in bookmark_avg_exercise_pairs:
            last_exercise = pair[1].past_exercises[-1:]
            if len(last_exercise) != 0:
                new_priority = algo_wrapper.calculate(last_exercise[0], i)
                pair[1].priority = new_priority
                print('{:+8.2f}'.format(new_priority), end=', ')

            if pair[1].priority > max_priority:
                next_bookmark = pair
                max_priority = pair[1].priority

        print('')



# if __name__ == "__mainq235__":
#
#     zeeguu.app = Flask("Zeeguu-Core-Test")
#
#     config_file = os.path.expanduser('../testing_default.cfg')
#     if "CONFIG_FILE" in os.environ:
#         config_file = os.environ["CONFIG_FILE"]
#     zeeguu.app.config.from_pyfile(config_file,
#                                   silent=False)  # config.cfg is in the instance folder
#
#     zeeguu.db = flask_sqlalchemy.SQLAlchemy(zeeguu.app)
#     print(("running with DB: " + zeeguu.app.config.get("SQLALCHEMY_DATABASE_URI")))
#
#     zeeguu.db.create_all()
#
#
#     ###########################################
#     ### correct - return after 10
#     ### incorrect - return after 3
#     user_id = 1
#     algo = ArtsRT()
#     algo.a
#     algo.b = 2
#     algo.D = 0
#     algo.r
#     algo.w = 15
#     algo_wrapper = AlgorithmWrapper(algo)
#
#     user = User.find_by_id(user_id)
#     bookmarks = user.all_bookmarks()
#
#     print('Using user '+user.name+' with id '+str(user.id))
#     print('Found '+str(len(bookmarks))+' bookmarks')
#
#     priority_infos = list()
#     for bookmark in bookmarks:
#         print(str(len(bookmark.exercise_log)), end=',')
#         for exercise in bookmark.exercise_log:
#             priority_infos.append(PriorityInfo(bookmark, exercise, PriorityInfo.MAX_PRIORITY))
#     print()
#
#     priority_infos_sorted = sorted(priority_infos, key=lambda x: x.exercise.time)
#
#     for i in range(0, len(priority_infos_sorted)):
#         print('{}'.format(priority_infos_sorted[i].exercise.id), end=',')
#     for i in range(0, len(priority_infos_sorted)):
#         max_exercise_id = 0
#         for j in range(0, i):
#             max_exercise_id = max([max_exercise_id, priority_infos_sorted[j].exercise.id])
#         #print('{}'.format(max_exercise_id), end=',')
#
#         for j in range(0, i):
#             new_priority = algo_wrapper.calculate(priority_infos_sorted[j].exercise, max_exercise_id)
#             priority_infos_sorted[i].priority=new_priority
#             print('{:+8.2f}'.format(new_priority), end=', ')
#         print('')
