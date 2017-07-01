from tests_core_zeeguu.rules.base_rule import BaseRule
from tests_core_zeeguu.rules.user_rule import UserRule
from zeeguu.model.cohort import Cohort
from zeeguu.model.teacher_cohort_map import TeacherCohortMap


class CohortRule(BaseRule):
    def __init__(self):
        super().__init__()
        self.cohort = self._create_model_object()
        self.save(self.cohort)

        self.teacher = UserRule().user
        self.save(self.teacher)

        teacher_role = TeacherCohortMap(self.teacher, self.cohort)
        self.save(teacher_role)

        self.student1 = UserRule().user
        self.student1.cohort = self.cohort
        self.save(self.student1)

        student2 = UserRule().user
        student2.cohort = self.cohort
        self.save(student2)

    def _create_model_object(self, *args):
        name = self.faker.word()
        cohort = Cohort(name)

        return cohort

    @staticmethod
    def _exists_in_db(obj):
        return Cohort.find(obj.id)
