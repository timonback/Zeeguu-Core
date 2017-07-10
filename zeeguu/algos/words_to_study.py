from zeeguu.algos.ab_testing import ABTesting
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.bookmark_priority_arts import BookmarkPriorityARTS


def bookmarks_to_study(user, desired_bookmarks_count=10):
    """Returns a list of bookmarks with the highest priorities

    If there are no bookmarks_groups (i.e. the bookmarks table is empty, or no Algorithms are declared in the
    WORD_SCHEDULING_ALGORITHM_CONFIG file) then an empty list is returned.

    Otherwise, an equal amount of bookmarks is taken from each bookmark_group and concatenated into a list,
    which is then returned. The amount of bookmarks taken from each group can differ by 1, depending on whether the
    possible_bookmarks_to_return_count is equally dividable by the group count.
    """
    bookmarks = Bookmark.query. \
        filter_by(user_id=user.id). \
        filter_by(learned=False). \
        join(BookmarkPriorityARTS). \
        filter(BookmarkPriorityARTS.bookmark_id == Bookmark.id). \
        order_by(BookmarkPriorityARTS.priority.desc()). \
        all()

    bookmark_groups = ABTesting.split_bookmarks_based_on_algorithm(bookmarks)
    if len(bookmarks) == 0 or len(bookmark_groups) == 0:
        return []

    bookmarks_to_return = []
    possible_bookmarks_to_return_count = min(desired_bookmarks_count, len(bookmarks))

    for i in range(possible_bookmarks_to_return_count):
        idx = i % len(bookmark_groups)
        bookmarks_to_return.append(bookmark_groups[idx].pop(0))

    return bookmarks_to_return
