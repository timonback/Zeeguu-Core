from faker import Faker
from sqlalchemy.exc import InvalidRequestError

import zeeguu.model


class BaseRule:
    faker = Faker()

    db = zeeguu.db

    @classmethod
    def save(cls, obj):
        try:
            cls.db.session.add(obj)
            cls.db.session.commit()
        except InvalidRequestError:
            cls.db.session.rollback()
            cls.save(obj)

    def _create_model_object(self):
        raise NotImplementedError

    @staticmethod
    def _exists_in_db(obj):
        raise NotImplementedError
