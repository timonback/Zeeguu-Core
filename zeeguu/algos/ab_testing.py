import configparser
import importlib

import zeeguu
import zeeguu.util.configuration as utils
from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper


class ABTesting:
    @staticmethod
    def create_algorithm(parameters):
        try:
            algorithm_name = parameters['type']
            del parameters['type']

            parameters_converted = {key: int(val) for (key, val) in parameters.items()}

            algorithm_class = getattr(importlib.import_module('zeeguu.algos.arts'), algorithm_name)
            return algorithm_class(**parameters_converted)

        except AttributeError as e:
            zeeguu.log('The specified algorithm class could not be found.')
            zeeguu.log(str(e))
            exit(-1)

    @staticmethod
    def get_dict_from_config(section):
        keys = [key for key in section]
        vals = [val for val in section.values()]
        return dict(zip(keys, vals))

    @staticmethod
    def load_algorithms(config):
        algorithms = []
        for s in config.sections():
            parameters = ABTesting.get_dict_from_config(config[s])
            new_algorithm = ABTesting.create_algorithm(parameters)
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

    @classmethod
    def split_bookmarks_based_on_algorithm(cls, bookmarks):
        groups = []
        for i in range(0, len(cls._algorithms)):
            groups.append([bookmarks[v] for v in range(i, len(bookmarks), len(cls._algorithms))])

        return groups