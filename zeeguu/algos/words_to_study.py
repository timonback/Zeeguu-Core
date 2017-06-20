from zeeguu.algos.ab_testing import ABTesting
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.bookmark_priority_arts import BookmarkPriorityARTS


def bookmarks_to_study(user, desired_bookmarks_count=10):
    bookmarks = Bookmark.query. \
        filter_by(user_id=user.id). \
        filter_by(learned=False). \
        join(BookmarkPriorityARTS). \
        filter(BookmarkPriorityARTS.bookmark_id == Bookmark.id). \
        order_by(BookmarkPriorityARTS.priority.desc()). \
        all()

    bookmark_groups = ABTesting.split_bookmarks_based_on_algorithm(bookmarks)
    if len(bookmark_groups) == 0:
        return []

    bookmarks_to_return = []
    desired_bookmarks_count_safe = min(desired_bookmarks_count, len(bookmarks))

    for i in range(0, desired_bookmarks_count_safe):
        idx = i % len(bookmark_groups)
        bookmarks_to_return.append(bookmark_groups[idx].pop(0))

    return bookmarks_to_return
