# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from app.settings import DevelopmentConfig
from app.controller.admin import bp as admin_bp
from app.controller.web import bp as web_bp
from app.controller.api import bp as api_bp
from app.extensions import dbm,dbs,login_manager,mail

#项目启动
def create_app(config=None):
    app = Flask(__name__)

    configure_app(app,config)
    configure_extentions(app)
    configure_blueprints(app)
    Bootstrap(app)

    return app
#导入配置文件
def configure_app(app,config):
    if not config:
        config = DevelopmentConfig

    app.config.from_object(config)
#导入插件
def configure_extentions(app):
    dbs.init_app(app)
    dbm.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
#导入蓝图
def configure_blueprints(app):
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(web_bp, url_prefix='')
    app.register_blueprint(api_bp,url_prefix='/api')