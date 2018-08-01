# -*- coding: utf-8 -*-

from app.service import BookService
from app.filter import admin_required

from flask_login import login_required

from . import bp
import json

@bp.route('/get/<string:itemlevel>/level/by/<string:itemvalue>',methods=['GET'])
def get_nextlevel_json_value(itemlevel,itemvalue):
    json_iteminfo=[]
    if itemlevel == 'second':
        unit_list = BookService.get_unit_by_book(itemvalue)
        for unit in unit_list:
            json_iteminfo.append(dict(zip(['itemvalue','itemname'],[unit.unit_id,unit.unit_name])))

    if itemlevel == 'third':
        section_list = BookService.get_section_by_unit(itemvalue)
        for section in section_list:
            json_iteminfo.append(dict(zip(['itemvalue','itemname'],[section.section_id,section.section_name])))

    jsonstr = {'itemInfo': json_iteminfo}
    return json.dumps(jsonstr)

@bp.route('/get/first/level',methods=['GET'])
def get_thislevel_json_value():
    json_iteminfo=[]
    book_list = BookService.get_books()

    for book in book_list:
        json_iteminfo.append(dict(zip(['itemvalue','itemname'],[book.book_id,book.book_name])))

    jsonstr = {'itemInfo': json_iteminfo}
    return json.dumps(jsonstr)