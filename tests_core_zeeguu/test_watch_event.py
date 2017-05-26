from datetime import datetime
from unittest import TestCase
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from zeeguu.model import Bookmark, WatchEventType, WatchInteractionEvent, UserActivityData

import zeeguu
db = zeeguu.db


class WatchEventTest(ModelTestMixIn, TestCase):

    def test_watch_event_type(self):
        retrieved = WatchEventType.find_by_name("glance")
        if not retrieved:
            retrieved = WatchEventType("glance")
            db.session.add(retrieved)
            db.session.commit()

        retrieved = WatchEventType.find_by_name("glance")
        assert retrieved.name == "glance"   
        return retrieved

    def test_watch_event(self):
        glance = self.test_watch_event_type()
        a_bookmark = Bookmark.find(1)

        new_glance = WatchInteractionEvent(glance, 1, datetime.now())
        db.session.add(new_glance)
        db.session.commit()

        assert len(WatchInteractionEvent.events_for_bookmark(a_bookmark)) == 1

    def test_user_activity_data(self):
        uad = UserActivityData(self.user,
                               datetime.now(),
                               "reading",
                               "1200",
                               "")
        assert uad.event == "reading"
        db.session.add(uad)
        db.session.commit()

    def test_get_user_activity_data(self):
        events = WatchInteractionEvent.events_for_user(self.user)
        assert len(events) == 0
        self.test_watch_event()
        events = WatchInteractionEvent.events_for_user(self.user)
        assert len(events) == 1
