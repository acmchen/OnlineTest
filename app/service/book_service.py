# -*- coding: utf-8 -*-
from app.models import BookInfo,SectionInfo,UnitInfo
from app.extensions import dbs

import uuid
'''书籍相关数据层'''
POST_PER_PAGE = 1
class BookService(object):
    #按书本名字与科目条件查询
    @staticmethod
    def search_bookinfo(bookinfo,page):
        query = BookInfo.query
        if bookinfo.has_key('bookname') and bookinfo['bookname']:
            query = query.filter(BookInfo.book_name.like('%'+bookinfo['bookname']+'%'))
        if bookinfo.has_key('subject') and bookinfo['subject']:
            query = query.filter(BookInfo.subject.like('%'+bookinfo['subject']+'%'))
        pagination = query.paginate(page,POST_PER_PAGE,error_out=False)
        return pagination
    #分页查询所有书籍信息
    @staticmethod
    def get_all_books(page):
        return BookInfo.query.paginate(page,POST_PER_PAGE,error_out=False)
    #非分页查询所有书籍信息
    @staticmethod
    def get_books():
        return BookInfo.query.all()
    #按书本id查询
    @staticmethod
    def get_book_by_id(book_id):
        return BookInfo.query.filter_by(book_id=book_id).first()
    #按单元id查询
    @staticmethod
    def get_unit_by_id(unit_id):
        return UnitInfo.query.filter_by(unit_id=unit_id).first()
    #按小节id查询
    @staticmethod
    def get_section_by_id(section_id):
        return SectionInfo.query.filter_by(section_id=section_id).first()
    #按书籍id查询从属于该书的所有单元
    @staticmethod
    def get_unit_by_book(book_id):
        unit_list = UnitInfo.query.filter_by(belong_to_book=book_id).order_by(dbs.asc(UnitInfo.unit_name)).all()
        return unit_list
    #按单元id查询从属于该单元的所有小节
    @staticmethod
    def get_section_by_unit(unit_id):
        section_list = SectionInfo.query.filter_by(belong_to_unit=unit_id).order_by(dbs.asc(SectionInfo.section_name)).all()
        return section_list
    #书籍信息更新
    @staticmethod
    def update_book(book_info,book_id):
        book = BookInfo.query.filter_by(book_id=book_id).first()
        book.book_name = book_info.book_name.data
        book.version = book_info.version.data
        book.author = book_info.author.data
        book.publisher = book_info.publisher.data
        book.publish_time = book_info.publish_time.data
        book.subject = book_info.subject.data
        dbs.session.commit()
    #章信息更新
    @staticmethod
    def update_unit(unit_info):
        unit = UnitInfo.query.filter_by(unit_id=unit_info.unit_id).first()
        unit.unit_name = unit_info.unit_name
        dbs.session.commit()
    #节信息更新
    @staticmethod
    def update_section(section_info):
        section = SectionInfo.query.filter_by(section_id=section_info.section_id).first()
        section.section_name = section_info.section_name
        dbs.session.commit()
    #添加书
    @staticmethod
    def add_book(book_info):
        book = BookInfo()
        book.book_id = str(uuid.uuid1())
        book.book_name = book_info.book_name.data
        book.version = book_info.version.data
        book.author = book_info.author.data
        book.publisher = book_info.publisher.data
        book.publish_time = book_info.publish_time.data
        book.subject = book_info.subject.data
        dbs.session.add(book)
        dbs.session.commit()
    #添加节
    @staticmethod
    def add_section(section_info):
        section_info.section_id = str(uuid.uuid1())
        dbs.session.add(section_info)
        dbs.session.commit()
    #添加单元
    @staticmethod
    def add_unit(unit_info):
        unit_info.unit_id = str(uuid.uuid1())
        dbs.session.add(unit_info)
        dbs.session.commit()
    #删除书
    @staticmethod
    def delete_book(book_id):
        book = BookInfo.query.filter_by(book_id=book_id).first()
        dbs.session.delete(book)
        dbs.session.commit()
    #删除单元
    @staticmethod
    def delete_section(section_id):
        section = SectionInfo.query.filter_by(section_id=section_id).first()
        dbs.session.delete(section)
        dbs.session.commit()
    #删除章
    @staticmethod
    def delete_unit(unit_id):
        unit = UnitInfo.query.filter_by(unit_id=unit_id).first()
        dbs.session.delete(unit)
        dbs.session.commit()
