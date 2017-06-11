# -*- coding: utf8 -*-
import datetime
import math
import os
import random

import flask_sqlalchemy
from flask import Flask

import zeeguu
from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper
from zeeguu.algos.arts.arts_rt import ArtsRT
from zeeguu.model import User, ExerciseOutcome, Exercise, ExerciseSource


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


class AverageExercise:
    def __init__(self, exercise_log):
        self.exercise_log = exercise_log
        self.past_exercises = []
        self.past_exercises_iteration = []

        self.avg_solving_speed, self.prob_correct = self._get_avg_exercise(exercise_log)

    @classmethod
    def _get_avg_exercise(cls, exercise_log):
        if len(exercise_log) == 0:
            return 500, 0.5

        avg_speed = mean([x.solving_speed for x in exercise_log])
        prob_correct = mean([x.outcome.correct for x in exercise_log])
        return avg_speed, prob_correct

    def append_new_exercise(self, iteration):
        random_outcome = ExerciseOutcome(
            ExerciseOutcome.CORRECT) if random.random() < self.prob_correct else ExerciseOutcome(ExerciseOutcome.WRONG)
        new_exercise = Exercise(random_outcome, ExerciseSource("Test"), self.avg_solving_speed, datetime.datetime.now())
        new_exercise.id = iteration
        self.past_exercises.append(new_exercise)
        self.past_exercises_iteration.append(iteration)
        return new_exercise


class CalculationHelper:
    def __init__(self, bookmark):
        self.bookmark = bookmark
        self.average_exercise = AverageExercise(bookmark.exercise_log)
        self.priority = 10


class Fancinator:
    correct_count_limit = 3
    removed_bookmark_priority = -1000

    def __init__(self, user_id, algorithm=None):
        self.user_id = user_id

        self.__create_database()

        if algorithm is None:
            algorithm = ArtsRT()
        self.algo_wrapper = AlgorithmWrapper(algorithm)

        self.bookmarks = self.__get_bookmarks_for_user(self.user_id)

    def __create_database(self):
        zeeguu.app = Flask("Zeeguu-Core-Test")

        config_file = os.path.expanduser('../testing_default.cfg')
        if "CONFIG_FILE" in os.environ:
            config_file = os.environ["CONFIG_FILE"]
        zeeguu.app.config.from_pyfile(config_file,
                                      silent=False)  # config.cfg is in the instance folder

        zeeguu.db = flask_sqlalchemy.SQLAlchemy(zeeguu.app)
        print(("running with DB: " + zeeguu.app.config.get("SQLALCHEMY_DATABASE_URI")))

        zeeguu.db.create_all()

    def set_algorithm_wrapper(self, new_algorithm_wrapper):
        self.algo_wrapper = new_algorithm_wrapper

    def calc_algorithm_stats(self, verbose=True):
        random.seed(0)

        calculation_helpers = self.__run_algorithm_on_bookmarks(self.bookmarks, verbose)
        return self.__calc_algorithm_result_stats(calculation_helpers)

    def __get_bookmarks_for_user(self, user_id):
        user = User.find_by_id(user_id)
        print('Using user ' + user.name + ' with id ' + str(user.id))
        return user.all_bookmarks()

    def __run_algorithm_on_bookmarks(self, bookmarks, verbose=True):
        if verbose:
            print('Found ' + str(len(bookmarks)) + ' bookmarks')

        calculation_helpers = [CalculationHelper(x) for x in bookmarks]
        next_bookmark = calculation_helpers[0]  # to know which exercise to generate next

        for i in range(0, 200):
            new_exercise = next_bookmark.average_exercise.append_new_exercise(i)
            if verbose:
                print("{:4} - {:} - {:1}".format(i, next_bookmark.bookmark.id, new_exercise.outcome.correct), end=', ')

            max_priority = 0
            for calculation_helper in calculation_helpers:
                last_exercises = calculation_helper.average_exercise.past_exercises[-self.correct_count_limit:]
                if len(last_exercises) != 0:
                    count_correct = math.fsum([x.outcome.correct for x in last_exercises])
                    if count_correct == self.correct_count_limit:
                        new_priority = self.removed_bookmark_priority
                    else:
                        new_priority = self.algo_wrapper.calculate(last_exercises[-1:][0], i)

                    calculation_helper.priority = new_priority
                    if verbose:
                        if new_priority != self.removed_bookmark_priority:
                            print('{:+8.2f}'.format(new_priority), end=', ')
                        else:
                            print('{:8}'.format(''), end=', ')

                if calculation_helper.priority > max_priority:
                    next_bookmark = calculation_helper
                    max_priority = calculation_helper.priority
            if verbose:
                print('')
        return calculation_helpers

    def __calc_algorithm_result_stats(self, calculation_helpers):
        repetition_correct = []  # bookmark, iterations
        repetition_incorrect = []
        for calculation_helper in calculation_helpers:
            average_exercise = calculation_helper.average_exercise
            for i in range(0, len(average_exercise.past_exercises_iteration) - 1):
                repetition_after = average_exercise.past_exercises_iteration[i + 1] - \
                                   average_exercise.past_exercises_iteration[i]
                if average_exercise.past_exercises[i].outcome.correct:
                    repetition_correct.append(repetition_after)
                else:
                    repetition_incorrect.append(repetition_after)

        repetition_correct_mean = mean(repetition_correct)
        repetition_incorrect_mean = mean(repetition_incorrect)

        print('Repetition of correct words on average for every   {:.4}, in raw: {:}'
              .format(repetition_correct_mean, repetition_correct))

        print('Repetition of incorrect words on average for every {:.4}, in raw: {:}'
              .format(repetition_incorrect_mean, repetition_incorrect))

        return [repetition_correct_mean, repetition_incorrect_mean]


class AlgorithmEvaluator:
    change_limit = 1.0

    def __init__(self, user_id, algorithm, max_iterations=20):
        self.fancy = Fancinator(user_id)
        self.algorithm = algorithm
        self.max_iterations = max_iterations

    def fit_algorithm(self, variables_to_set, diff_goal):
        iteration_counter = 0
        tick_tock = 0

        change = self.__run_algorithm_iteration(diff_goal)
        while change > self.change_limit or tick_tock != 0:
            print('------------------------------------------------------------------------')
            print('New iteration of the algorithm tickTock={}, variables={}'
                  .format(tick_tock, variables_to_set))

            new_variable_value = math.fabs(variables_to_set[tick_tock][1] + variables_to_set[tick_tock][2])
            setattr(self.algorithm, variables_to_set[tick_tock][0], new_variable_value)
            print('Trying now with D={}, b={}, w={}'.format(self.algorithm.D, self.algorithm.b, self.algorithm.w))
            self.__update_algorithm_instance(self.algorithm)
            # run the algorithm
            diff_to_goal = self.__run_algorithm_iteration(diff_goal)

            if diff_to_goal < change:
                print('Improvement found')

                # We just did better
                variables_to_set[tick_tock][1] = new_variable_value
                change = diff_to_goal
            else:
                print('No further improvement')

                # reset the variable
                setattr(self.algorithm, variables_to_set[tick_tock][0], variables_to_set[tick_tock][1])

                # Time to optimize on the other variable
                variables_to_set[tick_tock][2] *= -0.5

            tick_tock += 1
            tick_tock = divmod(tick_tock, len(variables_to_set))[1]

            iteration_counter = iteration_counter + 1
            if iteration_counter > self.max_iterations:
                print('Stopped due to max_iterations parameter')
                break
        return variables_to_set

    def __run_algorithm_iteration(self, diff_goal):
        result_new = self.fancy.calc_algorithm_stats(verbose=False)
        diff_new = self.__calc_diff(diff_goal, result_new)
        diff_to_goal = sum(diff_new)
        print('New diff to goal {} ({})'.format(diff_to_goal, diff_new))
        return diff_to_goal

    def __update_algorithm_instance(self, algorithm_instance):
        self.fancy.set_algorithm_wrapper(AlgorithmWrapper(algorithm_instance))

    @staticmethod
    def __calc_diff(a, b):
        if len(a) != len(b):
            raise ValueError('size of parameters is different: len(a): {} vs len(b): {}'.format(len(a), len(b)))

        diff = []
        for i in range(0, len(a)):
            diff.append(math.fabs(a[i] - b[i]))
        return diff


if __name__ == "__main__":
    user_id = 1
    # fancy = Fancinator(user_id)
    # fancy.calc_algorithm_stats()

    algorithm = ArtsRT()
    variables_to_set = [['D', getattr(algorithm, 'D'), +5], ['b', getattr(algorithm, 'b'), +10],
                        ['w', getattr(algorithm, 'w'), +10]]
    diff_goal = [15, 5]

    evaluator = AlgorithmEvaluator(user_id, algorithm)
    print(evaluator.fit_algorithm(variables_to_set, diff_goal))
