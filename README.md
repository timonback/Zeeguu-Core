# Zeeguu-Core [![Build Status](https://travis-ci.org/mircealungu/Zeeguu-Core.svg?branch=master)](https://travis-ci.org/mircealungu/Zeeguu-Core)

The main model behind the zeeguu infrastructure.


# Installation

Clone this repo

Create a new virtualenv

Run `python setup.py install` or, for development run `python setup.py develop`

You must set `ZEEGUU_CORE_CONFIG` as an environment variable
before you can run `import zeeguu`. For an example of how that
file should look look see `testing_default.cfg`. The config file
should contain login credentials to a DB that you will have to 
create.

The tests overwrite the `ZEEGUU_CORE_CONFIG` by setting it to 
`~/.config/zeeguu/core_test.cfg`. 

