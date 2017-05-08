from zeeguu.model import Bookmark, UserWord, BookmarkPriorityARTS


def bookmarks_to_study_new(user, desired_bookmarks_count=-1):
    bookmarks = Bookmark.query. \
        filter_by(user_id=user.id). \
        join(BookmarkPriorityARTS). \
        filter(BookmarkPriorityARTS.bookmark_id == Bookmark.id). \
        order_by(BookmarkPriorityARTS.priority.desc()). \
        limit(desired_bookmarks_count)

    # TODO: Filter by Bookmark.already_seen_today()
    return bookmarks


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

    return list(good_for_study)
