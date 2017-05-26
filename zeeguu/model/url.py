import re

import sqlalchemy.orm

import zeeguu
db = zeeguu.db

from zeeguu.model.domain_name import DomainName


class Url(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(2083))

    path = db.Column(db.String(2083))

    url = db.Column(db.String(2083))

    domain_name_id = db.Column(db.Integer, db.ForeignKey("domain_name.id"))
    domain = db.relationship(DomainName)

    def __init__(self, url, title):
        self.path = Url.get_path(url)
        self.domain = DomainName.find(Url.get_domain(url))
        self.title = title

    def title_if_available(self):
        if self.title != "":
            return self.title
        return self.url

    def as_string(self):
        return self.domain.domain_name + self.path

    def domain_name(self):
        return self.domain.domain_name

    @classmethod
    def get_domain(self, url):
        protocol_re = '(.*://)?'
        domain_re = '([^/?]*)'
        path_re = '(.*)'

        domain = re.findall(protocol_re + domain_re, url)[0]
        return domain[0] + domain[1]


    @classmethod
    def get_path(self, url):
        protocol_re = '(.*://)?'
        domain_re = '([^/?]*)'
        path_re = '(.*)'

        domain = re.findall(protocol_re + domain_re + path_re, url)[0]
        return domain[2]


    @classmethod
    def find(cls, url, title = ""):
        try:
            d = DomainName.find(Url.get_domain(url))
            return (cls.query.filter(cls.path == Url.get_path(url))
                             .filter(cls.domain == d)
                             .one())
        except sqlalchemy.orm.exc.NoResultFound:
            return cls(url, title)

    def render_link(self, link_text):
        if self.url != "":
            return '<a href="'+self.url+'">'+link_text+'</a>'
        else:
            return ""