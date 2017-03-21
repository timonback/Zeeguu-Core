# Zeeguu-Core

The main model behind the zeeguu infrastructure.

# Installation

1. create a zeeguu db
1. copy the `default_config.cfg` to `'~/.config/zeeguu/core.cfg'` and modify it accordinglty (especially the connection string to the zeeguu db)
1. create a new virtualenv
1. run `python setup.py [develop|install]` to deploy the zeeguu module in your local module folder
1. run `python populate.py` from the zeeguu folder to create a first version of the db
