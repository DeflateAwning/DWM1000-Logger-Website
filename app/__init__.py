#!/usr/bin/env python3

# app/__init__.py

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from flask_bcrypt import Bcrypt
#from flask_mail import Mail
from flask_migrate import Migrate # for database migrations/init


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # probably unused
#mail = Mail(app)
migrate = Migrate(app, db)


from app import routes