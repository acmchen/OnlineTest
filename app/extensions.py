#-*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_mail import Mail

#databases
dbs = SQLAlchemy()
dbm = MongoEngine()
#flask-login
login_manager = LoginManager()
login_manager.login_view = 'web.login'
#email
mail = Mail()

