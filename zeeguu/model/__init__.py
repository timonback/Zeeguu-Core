import flask_sqlalchemy
import zeeguu
from flask import Flask

from zeeguu.util.configuration import load_configuration_or_abort, assert_configs

# If zeeguu.app is already defined we use that object
# as the app for the db_init that we do later. If not,
# we create the app and load the corresponding configuration
if not hasattr(zeeguu, "app"):
    zeeguu.app = Flask("Zeeguu-Core")
    load_configuration_or_abort(zeeguu.app, 'ZEEGUU_CORE_CONFIG')


# Either local, or injected our app config should have at least these
assert_configs(zeeguu.app.config, ['SQLALCHEMY_DATABASE_URI', 'MAX_SESSION', 'SQLALCHEMY_TRACK_MODIFICATIONS'])


# Create the zeeguu.db object, which will be the superclass
# of all the model classes
zeeguu.db = flask_sqlalchemy.SQLAlchemy(zeeguu.app)
# Note, that if we pass the app here, then we don't need later
# to push the app context

# Creating the DB tables if needed
zeeguu.db.init_app(zeeguu.app)
zeeguu.db.create_all(app=zeeguu.app) 


print(('ZEEGUU: Linked model with: ' + zeeguu.app.config["SQLALCHEMY_DATABASE_URI"]))
