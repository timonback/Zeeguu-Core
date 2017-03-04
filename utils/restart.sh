#!/bin/bash
sudo python setup.py install
touch zeeguu.wsgi
sudo /etc/init.d/apache2 restart



