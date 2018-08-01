#-*- coding: utf-8 -*-

from flask_script import Manager
from flask_script import Server
from flask_script import prompt_bool

from app.settings import config
from app.application import create_app
from app.extensions import dbs,dbm

app = create_app(config['development'])

manager = Manager(app)

@manager.command
def initMysqlDb():
    "Creates  MySQL database tables"
    if prompt_bool("Are you sure? You will init your database"):
        dbs.create_all()

@manager.command
def dropMysqlDb():
    "Drops all MySQL database tables"
    if prompt_bool("Are you sure ? You will lose all your data!"):
        dbs.drop_all()

manager.add_command("runserver",Server(host='127.0.0.1',port='5000'))

if __name__ == '__main__':
    manager.run()