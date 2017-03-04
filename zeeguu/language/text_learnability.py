from zeeguu.the_librarian.text import split_words_from_text


def text_learnability(text, words_learning):
    """
    Computes the learnability of a given text -- that is, the number
    of words in the text that the user is learning at the moment

    :param text:
    :param words_learning:
    :return:
    """
    # Calculate learnability
    words = split_words_from_text(text['content'])
    words_learnability = []
    for word in words:
        if word in words_learning:
            words_learnability.append(word)
    count = len(words_learnability)
    learnability = count / float(len(words))
    return count, learnability