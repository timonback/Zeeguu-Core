# -*- coding: utf8 -*-
import os
import flask_sqlalchemy
from flask import Flask

# Initialize here the zeeguu.app because in several places
# in the zeeguu code it is expected especially for its config
# Also, the zeeguu.db which is a flask_sqlalchemy object
# requires the zeeguu.app for initialization
# In the future we should remove the dependnecy on flask_sqlalchemy

app = Flask("Zeeguu-Core")

# You always must setup the ZEEGUU_CORE_CONFIG before
# being able to import zeeguu
try:
    config_file = os.environ["ZEEGUU_CORE_CONFIG"]
    app.config.from_pyfile(config_file, silent=False)
except Exception as e:
    print (e)
    raise Exception("You must define a ZEEGUU_CORE_CONFIG environment var to be able to import zeeguu")


# BEGIN LINKING MODEL WITH DB
db = flask_sqlalchemy.SQLAlchemy(app)
import zeeguu.model
print ('Imported the zeeguu model linked with DB : ' + app.config["SQLALCHEMY_DATABASE_URI"])
# END LINKING MODEL WITH DB

