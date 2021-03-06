# Zeeguu-Core [![Build Status](https://travis-ci.org/mircealungu/Zeeguu-Core.svg?branch=master)](https://travis-ci.org/mircealungu/Zeeguu-Core) [![Coverage Status](https://coveralls.io/repos/github/mircealungu/Zeeguu-Core/badge.svg?branch=master)](https://coveralls.io/github/mircealungu/Zeeguu-Core?branch=master)

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

# Setup for Local Testing
1. Clone the project
2. Create a [new Virtual Environment](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv)
   1. Activate your Virtual Environment by running `source bin/activate` from within the Virtual Environment folder
3. Run `pip install mysql` (if you don't have MySQL installed already)
4. `cd` into the project folder
5. Run `python setup`
   1. Fix all the install exceptions.
6. Run `mysql -u root`
   1. Run `CREATE DATABASE zeeguu;`
   2. Run `exit`
6. Run `mysql.server start`
7. Open the `testing_default.cfg` file
   1. Change the value of `SQLALCHEMY_DATABASE_URI` from `("mysql://zeeguu_test:zeeguu_test@localhost/zeeguu_test")` to `("mysql://root@localhost/zeeguu")`
   2. Save and close `testing_default.cfg`
8. Let's check whether the Tests can be run and completed successfully.
   1. Make sure that the Virtual Environment is still active. Otherwise, redo Step 2.1
   2. `cd` into the project folder
   3. Run `./run_tests.sh`
   4. Check that all tests return 'ok'
9. Finally, lets populate the database
   1. From inside the project folder, run `mkdir -p ~/.config/zeeguu/ && cp testing_default.cfg ~/.config/zeeguu/core.cfg`
   2. Run `python zeeguu/populate.py`
   3. The database *should* be populated by now.

# MySQL

Install mysql and also the connection to python
```
apt-get install mysql-server libmysqlclient-dev python-mysqldb
```

# Project dev dependencies
```
apt-get install libxml2-dev libxslt1-dev
```
