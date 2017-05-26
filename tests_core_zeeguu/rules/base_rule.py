from faker import Faker

import zeeguu.model


class BaseRule:
    faker = Faker()

    db = zeeguu.db

    @classmethod
    def save(cls, obj):
        cls.db.session.add(obj)
        cls.db.session.commit()

    def _create_model_object(self):
        raise NotImplementedError

    @staticmethod
    def _exists_in_db(obj):
        raise NotImplementedError
