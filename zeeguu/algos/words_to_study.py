import zeeguu
from zeeguu.model import Bookmark, UserWord


def bookmarks_to_study(user, bookmark_count):
    """
    
    :param user: 
    :param bookmark_count: 
    :return: 
        
        list of bookmarks to study
        the list is empty if there's nothing to study
        
    """
    all_bookmarks = Bookmark.find_by_specific_user(user)

    good_for_study = set()
    size = 0
    for b in all_bookmarks:
        if b.good_for_study() and not b.already_seen_today():
            good_for_study.add(b)
            size += 1

        if size == bookmark_count:
            break

    if size < bookmark_count:
        # we did not find enough words to study which are ranked
        # add all the non-ranked ones, in chronological order

        all_bookmarks = Bookmark.query. \
            filter_by(user_id=user.id). \
            join(UserWord). \
            filter(UserWord.id == Bookmark.origin_id). \
            order_by(Bookmark.time.desc()).all()

        for b in all_bookmarks:
            if b.good_for_study() and not b.already_seen_today():
                good_for_study.add(b)
                size += 1

            if size == bookmark_count:
                break

    if size < bookmark_count:
        # we still don't have enough bookmarks.
        # in this case, we add some new ones to the user's account
        needed = bookmark_count - size
        from zeeguu.temporary.default_words import default_bookmarks
        new_bookmarks = default_bookmarks(user, user.learned_language_id)

        for each_new in new_bookmarks:
            # try to find if the user has seen this in the past
            good_for_study.add(each_new)
            zeeguu.db.session.add(each_new)
            size += 1

            if size == bookmark_count:
                break

    zeeguu.db.session.commit()


    return list(good_for_study)
