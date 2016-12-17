# coding: utf-8

import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                          'sqlite:///' + os.path.join(basedir, 'data-dev.db')
