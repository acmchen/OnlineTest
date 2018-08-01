from flask import Blueprint

bp = Blueprint('api',__name__)

from . import book_index_api