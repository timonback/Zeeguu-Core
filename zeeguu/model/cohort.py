import zeeguu
from sqlalchemy import Column, Integer, String


class Cohort(zeeguu.db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = Column(Integer, primary_key=True)

    name = Column(String(255))

    def __init__(self, name):
        self.name = name

    def get_students(self):
        from zeeguu.model.user import User
        return User.query.filter_by(cohort=self).all()

    def get_teachers(self):
        from zeeguu.model.teacher_cohort_map import TeacherCohortMap
        return TeacherCohortMap.get_teachers_for(self)

    @classmethod
    def find(cls, id):
        return cls.query.filter_by(id=id).one()