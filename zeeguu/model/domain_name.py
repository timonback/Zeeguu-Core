import re

import sqlalchemy.orm

import zeeguu
db = zeeguu.db


class DomainName(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}
    __tablename__ = 'domain_name'

    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(2083))

    def __init__(self, url):
        self.domain_name = self.extract_domain_name(url)

    def extract_domain_name(self, url):
        protocol_re = '(.*://)?'
        domain_re = '([^/?]*)'

        domain = re.findall(protocol_re + domain_re, url)[0]
        return domain[0] + domain[1]

    @classmethod
    def find(cls, domain_url):
        try:
            return (cls.query.filter(cls.domain_name == domain_url)
                             .one())
        except sqlalchemy.orm.exc.NoResultFound:
            # print "tried, but didn't find " + domain_url
            return cls(domain_url)