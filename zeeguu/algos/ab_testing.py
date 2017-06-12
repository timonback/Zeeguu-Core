import configparser

import zeeguu.util.configuration as utils
from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper
from zeeguu.algos.arts.arts_rt import ArtsRT


class ABTesting:
    @staticmethod
    def load_algorithms(config):
        algorithms = []
        for s in config.sections():
            new_algorithm = ArtsRT(
                    a=int(config[s]['a']),
                    D=int(config[s]['D']),
                    b=int(config[s]['b']),
                    r=int(config[s]['r']),
                    w=int(config[s]['w'])
            )
            algorithms.append(new_algorithm)

        return algorithms

    _config_file = utils.load_config_file('ALGORITHM_CONFIG_FILE')

    _config = configparser.ConfigParser()
    _config.read(_config_file)
    _algorithms = load_algorithms.__func__(_config)

    @classmethod
    def get_algorithm_for_id(cls, id):
        """Returns an algorithm specified in ALGORITHM_CONFIG_FILE based on the modulo
        of the ID of the object and the number of algorithms

        :param id: An Integer, for which the algorithm should be returned
        :return: An AlgorithmWrapper containing an ArtsRT object with the parameters
                 specified in ALGORITHM_CONFIG_FILE
        """
        count_algorithms = len(cls._algorithms)
        idx = divmod(id, count_algorithms)[1]
        return cls._algorithms[idx]

    @classmethod
    def get_algorithm_wrapper_for_id(cls, id):
        algorithm = cls.get_algorithm_for_id(id)
        return AlgorithmWrapper(algorithm)
