from zeeguu.model.bookmark import Bookmark
from zeeguu.model.bookmark_priority_arts import BookmarkPriorityARTS


def bookmarks_to_study(user, desired_bookmarks_count=-1):

    bookmarks = Bookmark.query. \
        filter_by(user_id=user.id). \
        join(BookmarkPriorityARTS). \
        filter(BookmarkPriorityARTS.bookmark_id == Bookmark.id). \
        order_by(BookmarkPriorityARTS.priority.desc()). \
        limit(desired_bookmarks_count)\
        .all()

    bookmarks = [each for each in bookmarks if not each.multiword_origin() ]

    # TODO: Filter by Bookmark.already_seen_today()
    return bookmarks
