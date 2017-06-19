import statistics


class NormalDistribution:
    @staticmethod
    def calc_normal_distribution(values):
        mean = statistics.mean(values)
        sd = statistics.stdev(values)
        return mean, sd
