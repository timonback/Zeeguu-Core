from tests_core_zeeguu.rules.base_rule import BaseRule
from tests_core_zeeguu.rules.bookmark_rule import BookmarkRule
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.language_rule import LanguageRule
from zeeguu.model.user import User


class UserRule(BaseRule):
    def __init__(self):
        super().__init__()

        self.user = self._create_model_object()

        self.save(self.user)

    def _create_model_object(self):
        random_email = self.faker.simple_profile()['mail']
        random_name = self.faker.name()
        random_password = self.faker.password()
        random_learned_language = LanguageRule().random
        random_native_language = LanguageRule().random

        while random_native_language.id == random_learned_language.id:
            random_native_language = LanguageRule().random

        user = User(random_email, random_name, random_password,
                    learned_language=random_learned_language,
                    native_language=random_native_language)

        if self._exists_in_db(user):
            return self._create_model_object()

        return user

    @staticmethod
    def _exists_in_db(obj):
        return User.exists(obj)

    def add_bookmarks(self, bookmark_count, exercises_count=0, **kwargs):
        bookmark_rules = []

        for _ in range(bookmark_count):
            bookmark_rule = BookmarkRule(self.user, **kwargs)
            bookmark = bookmark_rule.bookmark

            for i in range(0, exercises_count):
                random_exercise = ExerciseRule().exercise
                bookmark.add_new_exercise(random_exercise)

            bookmark_rules.append(bookmark_rule)
        return bookmark_rules
