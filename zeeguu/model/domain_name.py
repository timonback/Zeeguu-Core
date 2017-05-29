import re

from sqlalchemy.orm.exc import NoResultFound

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
        return cls.query.filter(DomainName.domain_name == domain_url).one()

    @classmethod
    def find_or_create(cls, domain_url):
        try:
            return cls.find(domain_url)
        except NoResultFound:
            return cls(domain_url)
