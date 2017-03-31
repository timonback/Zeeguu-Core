# Zeeguu-Core


The main model behind the zeeguu infrastructure.


# Installation


Create a zeeguu db

Create a new virtualenv

To install run `python setup.py install`

For development, run `python setup.py develop`

You must set `ZEEGUU_CORE_CONFIG` as an environment variable
before you can run `import zeeguu`. For an example of how that
file should look look see `testing_default.cfg`. 

Run `python populate.py` from the zeeguu folder to create a first version of the db


The tests overwrite the `ZEEGUU_CORE_CONFIG` by setting it to 
`~/.config/zeeguu/core_test.cfg`. 
