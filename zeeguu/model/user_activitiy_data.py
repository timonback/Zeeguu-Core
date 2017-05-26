import zeeguu
from zeeguu.model.user import User

db = zeeguu.db


class UserActivityData(db.Model):
    __table_args__ = dict(mysql_collate="utf8_bin")
    __tablename__ = 'user_activity_data'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(User)

    time = db.Column(db.DateTime)

    event = db.Column(db.String(255))
    value = db.Column(db.String(255))
    extra_data = db.Column(db.String(4096))

    def __init__(self, user, time, event, value, extra_data):
        self.user = user
        self.time = time
        self.event = event
        self.value = value
        self.extra_data = extra_data

    def data_as_dictionary(self):
        return dict(
                user_id=self.user_id,
                time=self.time.strftime("%Y-%m-%dT%H:%M:%S"),
                event=self.event,
                value=self.value,
                extra_data=self.extra_data
        )





