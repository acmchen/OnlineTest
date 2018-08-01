from flask import Blueprint

bp = Blueprint('web',__name__)

from . import auth
from . import exam_manage_web
from . import exam_list_web
from . import examing