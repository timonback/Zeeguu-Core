import flask_sqlalchemy
from flask import Flask
import zeeguu

app = Flask(__name__)
app.config.from_pyfile("zeeguu/tests/model_tests/testing.cfg", silent=True) #config.cfg is in the instance folder
zeeguu.db = flask_sqlalchemy.SQLAlchemy(app)

# Load all the model classes, so they see the db object
import zeeguu.model

from zeeguu.populate import create_minimal_test_db
create_minimal_test_db(zeeguu.db)

from zeeguu.model import User, Language

mir = User.find("i@mir.lu")
print (mir)

en = Language.find("en")
print (en)
