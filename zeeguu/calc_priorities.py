# -*- coding: utf8 -*-
import datetime
import math
import os
import random

import flask_sqlalchemy
from flask import Flask

import zeeguu
from zeeguu.algos.algo_service import PriorityInfo
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
        self.priorities = []

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
                new_priority = PriorityInfo.MAX_PRIORITY

                last_exercises = calculation_helper.average_exercise.past_exercises[-self.correct_count_limit:]
                if len(last_exercises) != 0:
                    count_correct = math.fsum([x.outcome.correct for x in last_exercises])
                    if count_correct == self.correct_count_limit:
                        new_priority = self.removed_bookmark_priority
                    else:
                        new_priority = self.algo_wrapper.calculate(last_exercises[-1:][0], i)
                    calculation_helper.average_exercise.priorities.append([i, new_priority])

                    if verbose:
                        if new_priority != self.removed_bookmark_priority:
                            print('{:+8.2f}'.format(new_priority), end=', ')
                        else:
                            print('{:8}'.format(''), end=', ')

                if new_priority > max_priority:
                    next_bookmark = calculation_helper
                    max_priority = new_priority
            if verbose:
                print('')
        return calculation_helpers

    def __calc_algorithm_result_stats(self, calculation_helpers):
        words_in_parallel = [0 for _ in calculation_helpers]
        repetition_correct = []  # bookmark, iterations
        repetition_incorrect = []
        for calculation_helper in calculation_helpers:
            average_exercise = calculation_helper.average_exercise
            for priority_iteration in average_exercise.priorities:
                if priority_iteration[1] != self.removed_bookmark_priority:
                    words_in_parallel[priority_iteration[0]] += 1

            for i in range(0, len(average_exercise.past_exercises_iteration) - 1):
                repetition_after = average_exercise.past_exercises_iteration[i + 1] - \
                                   average_exercise.past_exercises_iteration[i]
                if average_exercise.past_exercises[i].outcome.correct:
                    repetition_correct.append(repetition_after)
                else:
                    repetition_incorrect.append(repetition_after)

        # remove all words that have not been covered at all
        words_in_parallel = list(filter((0).__ne__, words_in_parallel))

        words_in_parallel_mean = mean(words_in_parallel)
        repetition_correct_mean = mean(repetition_correct)
        repetition_incorrect_mean = mean(repetition_incorrect)

        print('Concurrent words on average                        {:.4}, in raw: {:}'
              .format(words_in_parallel_mean, words_in_parallel))

        print('Repetition of correct words on average for every   {:.4}, in raw: {:}'
              .format(repetition_correct_mean, repetition_correct))

        print('Repetition of incorrect words on average for every {:.4}, in raw: {:}'
              .format(repetition_incorrect_mean, repetition_incorrect))

        return [words_in_parallel_mean, repetition_correct_mean, repetition_incorrect_mean]


class OptimizationGoals:
    def __init__(self,
                 words_in_parallel=10, words_in_parallel_factor=1.0,
                 repetition_correct=15, repetition_correct_factor=1.0,
                 repetition_incorrect=5, repetition_incorrect_factor=1.0):
        '''
        Used to specifiy on which goals to focus during the algorithm evalulation
        :param words_in_parallel: Amount of words to study in parallel
        :param words_in_parallel_factor: Weighting factor (higher=more important [relative to the others])
        :param repetition_correct: After x words, correct words should reappear
        :param repetition_correct_factor: Weighting factor (higher=more important [relative to the others])
        :param repetition_incorrect: After x words, incorrect words should reappear
        :param repetition_incorrect_factor: Weighting factor (higher=more important [relative to the others])
        '''
        self.words_in_parallel = words_in_parallel
        self.words_in_parallel_factor = words_in_parallel_factor
        self.repetition_correct = repetition_correct
        self.repetition_correct_factor = repetition_correct_factor
        self.repetition_incorrect = repetition_incorrect
        self.repetition_incorrect_factor = repetition_incorrect_factor

class AlgorithmEvaluator:
    def __init__(self, user_id, algorithm, max_iterations=20, change_limit=1.0):
        self.fancy = Fancinator(user_id)
        self.algorithm = algorithm
        self.max_iterations = max_iterations
        self.change_limit = change_limit

    def fit_parameters(self, variables_to_set, optimization_goals):
        iteration_counter = 0
        tick_tock = 0

        # Init run
        result_new = self.fancy.calc_algorithm_stats(verbose=False)
        change = self.__diff_to_goal(optimization_goals, result_new)

        while change > self.change_limit or tick_tock != 0:
            print('------------------------------------------------------------------------')
            print('New iteration of the algorithm tickTock={}, variables={}'
                  .format(tick_tock, variables_to_set))

            new_variable_value = math.fabs(variables_to_set[tick_tock][1] + variables_to_set[tick_tock][2])
            setattr(self.algorithm, variables_to_set[tick_tock][0], new_variable_value)
            print('Trying now with D={}, b={}, w={}'.format(self.algorithm.D, self.algorithm.b, self.algorithm.w))
            self.__update_algorithm_instance(self.algorithm)

            # run the algorithm
            result_new = self.fancy.calc_algorithm_stats(verbose=False)
            diff_to_goal = self.__diff_to_goal(optimization_goals, result_new)

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

        print('')
        print('The variables should be set the following way:')
        for variable_to_set in variables_to_set:
            print('{}={}'.format(variable_to_set[0], variable_to_set[1]))

        return variables_to_set

    def __update_algorithm_instance(self, algorithm_instance):
        self.fancy.set_algorithm_wrapper(AlgorithmWrapper(algorithm_instance))

    def __diff_to_goal(self, optimization_goals, result_new):
        # corresponds to the output from __calc_algorithm_result_stats()
        optimization_list = [
            optimization_goals.words_in_parallel,
            optimization_goals.repetition_correct,
            optimization_goals.repetition_incorrect
        ]
        optimization_list_factors = [
            optimization_goals.words_in_parallel_factor,
            optimization_goals.repetition_correct_factor,
            optimization_goals.repetition_incorrect_factor
        ]

        diffs = self.__calc_diff(result_new, optimization_list, optimization_list_factors)
        result = math.fsum(diffs)
        print('              concurrent words: {:6.4f}, correct words: {:6.4f}, incorrect words: {:6.4f}'.
              format(result_new[0], result_new[1], result_new[2]))
        print('Diff: {:6.4f}, concurrent words: {:6.4f}, correct words: {:6.4f}, incorrect words: {:6.4f}'.
              format(result, diffs[0], diffs[1], diffs[2]))
        return result

    @staticmethod
    def __calc_diff(a, b, factor=None):
        if len(a) != len(b):
            raise ValueError('size of parameters is different: len(a): {} vs len(b): {}'.format(len(a), len(b)))
        if factor is None:
            factor = [1 for _ in range(0, (len(a)))]

        diffs = []
        for i in range(0, len(a)):
            diff = math.fabs(a[i] - b[i])
            diffs.append(diff * factor[i])
        return diffs


if __name__ == "__main__":
    user_id = 1
    # fancy = Fancinator(user_id)
    # fancy.calc_algorithm_stats()

    algorithm = ArtsRT()
    variables_to_set = [['D', getattr(algorithm, 'D'), +5], ['b', getattr(algorithm, 'b'), +10],
                        ['w', getattr(algorithm, 'w'), +10]]
    optimization_goals = OptimizationGoals(
        words_in_parallel=30, words_in_parallel_factor=3,
        repetition_correct_factor=0,
        repetition_incorrect_factor=0
    )

    evaluator = AlgorithmEvaluator(user_id, algorithm, change_limit=1.0)
    print(evaluator.fit_parameters(variables_to_set, optimization_goals))
