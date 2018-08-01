from flask import Blueprint

bp = Blueprint('admin',__name__)

from . import auth
from . import user_manage
from . import book_manage
from . import problem_manage
from . import exam_manage