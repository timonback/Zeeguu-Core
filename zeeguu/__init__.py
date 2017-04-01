# -*- coding: utf8 -*-
import flask_sqlalchemy
from flask import Flask
from zeeguu.util.configuration import load_configuration_or_abort

# Initialize here the zeeguu.app because in several places
# in the zeeguu code it is expected especially for its config
# Also, the zeeguu.db which is a flask_sqlalchemy object
# requires the zeeguu.app for initialization
# In the future we should remove the dependnecy on flask_sqlalchemy

app = Flask("Zeeguu-Core")

load_configuration_or_abort(app, 'ZEEGUU_CORE_CONFIG',
                            ['SQLALCHEMY_DATABASE_URI', 'MAX_SESSION', 'SQLALCHEMY_TRACK_MODIFICATIONS'])


# BEGIN LINKING MODEL WITH DB
db = flask_sqlalchemy.SQLAlchemy(app)
import zeeguu.model
print ('Zeeguu model linked with: ' + app.config["SQLALCHEMY_DATABASE_URI"])
# END LINKING MODEL WITH DB

