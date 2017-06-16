import math


class NormalDistribution:

    @staticmethod
    def calc_normal_distribution(values):
        mean = NormalDistribution.mean(values)
        sd = NormalDistribution.calc_standard_deviation(values, mean)
        return mean, sd

    @staticmethod
    def calc_standard_deviation(values, mean):
        if len(values) == 0:
            return None

        s = sum([(val - mean) ** 2 for val in values])

        avg = s / len(values)
        sd = math.sqrt(avg)
        return sd

    @staticmethod
    def mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

