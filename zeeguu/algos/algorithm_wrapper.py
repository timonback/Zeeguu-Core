from zeeguu.model.learner_stats.exercise_stats import ExerciseStats


class AlgorithmWrapper:

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def __eq__(self, other):
        return self.algorithm == other.algorithm

    def calculate(self, exercise, max_iterations):
        if exercise is None:
            raise ValueError("Exercise must not be None")

        args = self._args_prepare(exercise, max_iterations)
        return self.algorithm.calculate(args)

    def _args_prepare(self, exercise, max_iterations):
        N = max_iterations - exercise.id
        alpha = not exercise.outcome.correct
        RT = exercise.solving_speed
        return N, alpha, RT


class AlgorithmSDCaller(AlgorithmWrapper):
    def _args_prepare(self, exercise, max_iterations):
        N = max_iterations - exercise.id
        alpha = exercise.outcome.correct
        sd = self.convert_rt_to_sd(exercise)

        return N, alpha, sd

    def convert_rt_to_sd(self, exercise):
        exercise_stats = ExerciseStats.query().filter_by(exercise_source_id=exercise.source_id).one()
        return (exercise.solving_speed - exercise_stats.mean) / exercise_stats.sd
