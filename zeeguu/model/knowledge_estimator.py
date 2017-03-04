import flask

import zeeguu
db = zeeguu.db
from zeeguu.model.exercise_based_probability import ExerciseBasedProbability
from zeeguu.model.encounter_based_probability import EncounterBasedProbability
from zeeguu.model.known_word_probability import KnownWordProbability
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.language import Language
from zeeguu.model.ranked_word import RankedWord


class SethiKnowledgeEstimator(object):
    """
    Computes statistics about this user.
     
    """

    def __init__(self, user, lang_code = None):
        self.user = user
        if lang_code:
            self.lang_code = lang_code
        else:
            self.lang_code = self.user.learned_language_id
        self.language = Language.find(self.lang_code)

    def known_words_list(self):
        lang_id = Language.find(self.lang_code)
        bookmarks = self.user.all_bookmarks()
        known_words = []
        filtered_known_words_from_user = []
        filtered_known_words_dict_list = []
        for bookmark in bookmarks:
            if bookmark.check_is_latest_outcome_too_easy():
                known_words.append(bookmark.origin.word)

        # for word_known in known_words:
        #     if RankedWord.exists(word_known, lang_id):
        #         filtered_known_words_from_user.append(word_known)
        #         # zeeguu.db.session.commit()
        # filtered_known_words_from_user = list(set(filtered_known_words_from_user))
        # for word in filtered_known_words_from_user:
        #     filtered_known_words_dict_list.append({'word': word})
        # return filtered_known_words_dict_list

        return known_words

    def get_known_bookmarks(self):
        """
        All the bookmarks that the user knows and are in a given language
        :param user:
        :param lang:
        :return:
        """
        bookmarks = self.user.all_bookmarks()
        known_bookmarks=[]
        for bookmark in bookmarks:
            if bookmark.check_is_latest_outcome_too_easy() and self.language == bookmark.origin.language:
                    known_bookmark_dict = {
                        'id': bookmark.id,
                        'origin': bookmark.origin.word,
                        'text': bookmark.text.content,
                        'time': bookmark.time.strftime('%m/%d/%Y')}
                    known_bookmarks.append(known_bookmark_dict)
        return known_bookmarks

    def get_known_bookmarks_count(self):
        return len(self.get_known_bookmarks())

    # MAKES NO SENSE TO HAVE BOTH Known Bookmarks and LEarned Bookmarks
    def learned_bookmarks(self):
        """
        Returns the bookmarks that the user has learned.
        :param user:
        :param lang:
        :return: list of bookmarks
        """
        bookmarks = self.user.all_bookmarks()
        too_easy_bookmarks = []
        for bookmark in bookmarks:
            if bookmark.check_is_latest_outcome_too_easy() and bookmark.origin.language == self.language:
                too_easy_bookmarks.append(bookmark)
        return [bookmark for bookmark in bookmarks if bookmark not in too_easy_bookmarks]

    def get_not_encountered_words(self):
        not_encountered_words_dict_list = []
        all_ranks = RankedWord.find_all(self.language)
        known_word_probs = KnownWordProbability.find_all_by_user_with_rank(self.user)
        for p in known_word_probs:
            if p.ranked_word in all_ranks:
                all_ranks.remove(p.ranked_word)
        for rank in all_ranks:
            not_encountered_word_dict = {}
            not_encountered_word_dict['word'] = rank.word
            not_encountered_words_dict_list.append(not_encountered_word_dict)
        return not_encountered_words_dict_list

    def get_not_encountered_words_count(self):
        return len(self.get_not_encountered_words())

    # TODO: remove the stupid dictionaries from the result list
    def get_not_looked_up_words(self):
        enc_probs = EncounterBasedProbability.find_all_by_user(self.user)
        words = [prob.ranked_word.word for prob in enc_probs
                 if prob.ranked_word.language == self.language
                 and prob.probability > 0.7]
        return words

    def get_not_looked_up_words_for_learned_language(self):
        return self.get_not_looked_up_words()

    def get_not_looked_up_words_count(self):
        return len(self.get_not_looked_up_words_for_learned_language())

    def get_probably_known_words(self):
        # TODO: Why the hell does this function return a dict with one key named word???
        probabilities = KnownWordProbability.get_probably_known_words(self.user)
        words = [probability.get_word_form() for probability in probabilities]
        return words


    def get_probably_known_words_count(self):
        return len(self.get_probably_known_words())

    def get_lower_bound_percentage_of_basic_vocabulary(self):
        high_known_word_prob_of_user = KnownWordProbability.get_probably_known_words(self.user)
        count_high_known_word_prob_of_user_ranked = 0
        for prob in high_known_word_prob_of_user:
            if prob.ranked_word is not None and prob.ranked_word.rank <=3000:
                count_high_known_word_prob_of_user_ranked +=1
        return round(float(count_high_known_word_prob_of_user_ranked)/3000*100,2)

    def get_upper_bound_percentage_of_basic_vocabulary(self):
        count_not_looked_up_words_with_rank = 0
        not_looked_up_words = EncounterBasedProbability.find_all_by_user(self.user)
        for prob in not_looked_up_words:
            if prob.ranked_word.rank <=3000:
                count_not_looked_up_words_with_rank +=1
        return round(float(count_not_looked_up_words_with_rank)/3000*100,2)

    def get_lower_bound_percentage_of_extended_vocabulary(self):
        high_known_word_prob_of_user = KnownWordProbability.get_probably_known_words(self.user)
        count_high_known_word_prob_of_user_ranked = 0
        for prob in high_known_word_prob_of_user:
            if prob.ranked_word is not None and prob.ranked_word.rank <=10000:
                count_high_known_word_prob_of_user_ranked +=1
        return round(float(count_high_known_word_prob_of_user_ranked)/10000*100,2)

    def get_upper_bound_percentage_of_extended_vocabulary(self):
        count_not_looked_up_words_with_rank = 0
        not_looked_up_words = EncounterBasedProbability.find_all_by_user(self.user)
        for prob in not_looked_up_words:
            if prob.ranked_word.rank <=10000:
                count_not_looked_up_words_with_rank +=1
        return round(float(count_not_looked_up_words_with_rank)/10000*100,2)

    def get_percentage_of_probably_known_bookmarked_words(self):
        high_known_word_prob_of_user = KnownWordProbability.get_probably_known_words(self.user)
        count_high_known_word_prob_of_user =0
        count_bookmarks_of_user = len(self.user.all_bookmarks())
        for prob in high_known_word_prob_of_user:
            if prob.user_word is not None:
                count_high_known_word_prob_of_user +=1
        if count_bookmarks_of_user <> 0:
            return round(float(count_high_known_word_prob_of_user)/count_bookmarks_of_user*100,2)
        else:
            return 0

    def words_being_learned(self, language):
        # Get the words the user is currently learning
        words_learning = {}
        bookmarks = Bookmark.find_by_specific_user(self.user)
        for bookmark in bookmarks:
            learning = not bookmark.check_is_latest_outcome_too_easy()
            user_word = bookmark.origin
            if learning and user_word.language == language:
                words_learning[user_word.word] = user_word.word
        return words_learning


def update_probabilities_for_word(word):

    try:
        bookmarks_for_this_word = Bookmark.find_all_by_user_and_word(flask.g.user, word)

        ex_prob = ExerciseBasedProbability.find_or_create(flask.g.user, word)
        total_prob = 0
        for b in bookmarks_for_this_word:
            ex_prob.calculate_known_bookmark_probability(b)
            total_prob += float(ex_prob.probability)
        ex_prob.probability = total_prob / len(bookmarks_for_this_word)
        print "!ex_prob: " + str(ex_prob.probability)

        if RankedWord.exists(word.word, word.language):
            ranked_word = RankedWord.find(word.word, word.language)
            if EncounterBasedProbability.exists(flask.g.user, ranked_word):
                enc_prob = EncounterBasedProbability.find(flask.g.user, ranked_word)
                known_word_prob = KnownWordProbability.find(flask.g.user, word, ranked_word)
                print "!known word prob before: " + str(known_word_prob.probability)
                print "!enc_prob: " + str(enc_prob.probability)
                known_word_prob.probability = KnownWordProbability.calculate_known_word_prob(ex_prob.probability,
                                                                                             enc_prob.probability)
                print "!known word prob after: " + str(known_word_prob.probability)
            else:
                known_word_prob = KnownWordProbability.find(flask.g.user, word, ranked_word)
                known_word_prob.probability = ex_prob.probability

        db.session.commit()
    except:
        print "failed to update probabilities for word with id: " + str(word.id)

    print "!successfully updated probabilities for word with id {0}".format(word.id)
