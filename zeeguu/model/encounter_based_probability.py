import sqlalchemy.orm

import zeeguu
db = zeeguu.db
from zeeguu.model.ranked_word import RankedWord


class EncounterBasedProbability(db.Model):
    __tablename__ = 'encounter_based_probability'
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    DEFAULT_PROBABILITY = 0.5

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    user = db.relationship("User")
    ranked_word_id = db.Column(db.Integer, db.ForeignKey("ranked_word.id"), nullable=False)
    ranked_word = db.relationship("RankedWord")
    not_looked_up_counter = db.Column(db.Integer,nullable = False)
    probability = db.Column(db.DECIMAL(10,9), nullable = False)
    db.UniqueConstraint(user_id, ranked_word_id)
    db.CheckConstraint('probability>=0', 'probability<=1')

    def __init__(self, user, ranked_word, not_looked_up_counter, probability):
        self.user = user
        self.ranked_word = ranked_word
        self.not_looked_up_counter = not_looked_up_counter
        self.probability = probability

    @classmethod
    def find(cls, user, ranked_word, default_probability=None):
         try:
            return cls.query.filter_by(
                user = user,
                ranked_word = ranked_word
            ).one()
         except  sqlalchemy.orm.exc.NoResultFound:
            return cls(user, ranked_word, 1, default_probability)

    @classmethod
    def find_all(cls):
        return cls.query.all()



    @classmethod
    def find_all_by_user(cls, user):
        return cls.query.filter_by(
            user = user
        ).all()

    @classmethod
    def exists(cls, user, ranked_word):
         try:
            cls.query.filter_by(
                user = user,
                ranked_word = ranked_word
            ).one()
            return True
         except sqlalchemy.orm.exc.NoResultFound:
            return False

    # TODO: Must rename to find_or_create_and_update
    @classmethod
    def find_or_create(cls, word, user, language):
        ranked_word = RankedWord.find(word.lower(), language)
        if EncounterBasedProbability.exists(user, ranked_word):
            enc_prob = EncounterBasedProbability.find(user,ranked_word)
            enc_prob.not_looked_up_counter +=1
            enc_prob.boost_prob()
        else:
            enc_prob = EncounterBasedProbability.find(user,ranked_word, EncounterBasedProbability.DEFAULT_PROBABILITY)
        return enc_prob

    @classmethod
    def find_for_userword(cls, user, userword):
        if RankedWord.exists(userword.word, userword.language):
            ranked_word = RankedWord.find(userword.word, userword.language)
            if EncounterBasedProbability.exists(user, ranked_word):
                enc_prob = EncounterBasedProbability.find(user, ranked_word)
                return enc_prob
        return None

    def reset_prob (self):
        # Why is this 0.5? Should be lower! I just looked up the word...
        # ugh...
        self.probability = 0.5

    def word_has_just_beek_bookmarked(self):
        """
            the user can't know this word very well if he's
            bookmarking it again
        :return:
        """

        self.probability /= 2

#         This function controls if prob is already 1.0, else it adds 0.1. It maximum adds 0.1, therefore cannot exceed 1
    def boost_prob(self):
        if float(self.probability) <> 1.0:
            self.probability = float(self.probability) + 0.1