from zeeguu.algos.arts.arts_rt import ArtsRT

from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper


class ABTesting:

    algorithm_a = AlgorithmWrapper(ArtsRT(
            a=0.1,
            D=2,
            b=1.1,
            r=1.7,
            w=20
    ))

    algorithm_b = AlgorithmWrapper(ArtsRT(
            a=0.1,
            D=3,
            b=4,
            r=2,
            w=200
    ))

    @classmethod
    def get_algorithm_based_on_user(cls, user):
        if divmod(user.id, 2):
            return cls.algorithm_a
        else:
            return cls.algorithm_b
