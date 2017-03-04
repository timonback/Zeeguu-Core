# -*- coding: utf8 -*-
#
# This file encapsulates the algorithm for computing the difficulty of
# a given text taking.
#
# The algorithm was extracted from a really impressive single method
# that used to live in the /get_difficulty_for_text endpoint implementation
#
# Original algo implementation was initially written by Linus Schab
#
# __author__ = 'mircea'
#

from zeeguu.the_librarian.text import split_words_from_text
from zeeguu.model.ranked_word import RankedWord


REFERENCE_VOCABULARY_SIZE = 10000.0

def discrete_text_difficulty(median_difficulty, average_difficulty):
    """

    :param median_difficulty:
    :param average_difficulty:
    :return: a symbolic representation of the estimated difficulty
     the values are between "EASY", "MEDIUM", and "HARD"
    """
    if (average_difficulty < 0.3):
        return "EASY"
    if (average_difficulty < 0.4):
        return "MEDIUM"
    return "HARD"


def text_difficulty(text, language, known_probabilities, difficulty_computer = 'default', rank_boundary = REFERENCE_VOCABULARY_SIZE):
    """
    :param known_probabilities: the probabilities that the user knows individual words
    :param language: the learned language
    :param difficulty_computer: if known the name of the algo used to compute the difficulty.
        currently only default is implemented
    :param personalized (deprecated)
    :param rank_boundary: 10.000 words
    :param text: text to analyse
    :return: a dictionary with three items for every text:
      1. score_average - average difficulty of the words in the text
      2. score_median - median difficulty of the words in the text
      3. estimated_difficulty - oen of three "EASY", "MEDIUM", "HARD"
    """
    word_difficulties = []

    # Calculate difficulty for each word
    words = split_words_from_text(text)

    for word in words:
        ranked_word = RankedWord.find_cache(word, language)
        difficulty = word_difficulty(known_probabilities, True, rank_boundary, ranked_word, word)
        word_difficulties.append(difficulty)

    # If we can't compute the text difficulty, we estimate hard
    if (len(word_difficulties)) == 0:
        return \
            dict(
                score_median=1,
                score_average=1,
                estimated_difficulty=1)

    # Average difficulty for text
    difficulty_average = sum(word_difficulties) / float(len(word_difficulties))

    # Median difficulty
    word_difficulties.sort()
    center = int(round(len(word_difficulties) / 2, 0))
    difficulty_median = word_difficulties[center]

    difficulty_scores = dict(
        score_median=difficulty_median,
        score_average=difficulty_average,
        estimated_difficulty=discrete_text_difficulty(difficulty_average, difficulty_median))

    return difficulty_scores


def word_difficulty(known_probabilities, personalized, rank_boundary, ranked_word, word):
    """
    # estimate the difficulty of a word, given:
        :param known_probabilities:
        :param personalized:
        :param rank_boundary:
        :param ranked_word:
        :param word:

    :return: a normalized value where 0 is (easy) and 1 is (hard)
    """

    # Assume word is difficult and unknown
    estimated_difficulty = 1.0

    if not ranked_word:
        return estimated_difficulty

    # Check if the user knows the word
    try:
        known_probability = known_probabilities[word]  # Value between 0 (unknown) and 1 (known)
    except KeyError:
        known_probability = None

    if personalized and known_probability is not None:
        estimated_difficulty -= float(known_probability)
    elif ranked_word.rank <= rank_boundary:
        word_frequency = (rank_boundary - (
            ranked_word.rank - 1)) / rank_boundary  # Value between 0 (rare) and 1 (frequent)
        estimated_difficulty -= word_frequency
    return estimated_difficulty

