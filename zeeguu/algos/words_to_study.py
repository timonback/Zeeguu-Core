from zeeguu.model.bookmark import Bookmark
from zeeguu.model.bookmark_priority_arts import BookmarkPriorityARTS


def bookmarks_to_study(user, desired_bookmarks_count=-1):
    bookmarks = Bookmark.query. \
        filter_by(user_id=user.id). \
        filter_by(learned=False). \
        join(BookmarkPriorityARTS). \
        filter(BookmarkPriorityARTS.bookmark_id == Bookmark.id). \
        order_by(BookmarkPriorityARTS.priority.desc()). \
        all()

    return bookmarks[:desired_bookmarks_count]
