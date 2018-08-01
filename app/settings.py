#-*- coding: utf-8 -*-
import os

class Config(object):
    
    DEBUG = False
    TESTING = False

    #mail settings
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'

    MAIL_USERNAME = 'sdutonlinetest@163.com'
    MAIL_PASSWORD = 'acm506onlinetest'

    #base settings
    IS_REGISTER = {0:u'不开启',1:u'开启'}
    IS_HIDDEN = {0:u'开放',1:u'隐藏'}
    PROBLEM_TYPE = {'choice':'1','blank':'2','short_answer':'3'}
    PROBLEM_TYPE_HTML = {'1':u'选择题','2':u'填空题','3':u'简答题'}
    USER_LEVEL = {1:u'学生',2:u'教师',3:u'管理员'}
    STATUS = {0:u'禁用',1:u'启用'}
    ADMIN_PAGE_ACTIVE = {'user':'user','problem':'problem','exam':'exam'}

class DevelopmentConfig(Config):

    ENV = 'development'
    DEBUG = True

    DEFAULT_PASSWORD = 'OT123456'

    #session
    CSRF_ENABLED = True
    SECRET_KEY = "titeguoytisseuguoy"

    #MysqlDb
    SQLALCHEMY_DATABASE_URI = "mysql://root:123@127.0.0.1/OnlineTest"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #MongoDb
    MONGODB_SETTINGS = {
        'db':'OnlineTest',
        'host': '127.0.0.1',
        'port': 27017
        }

config = {
    'development':DevelopmentConfig
    }