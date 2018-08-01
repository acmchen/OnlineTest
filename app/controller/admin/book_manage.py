# -*- coding: utf-8 -*-
from app.models import BookInfo,SectionInfo,UnitInfo
from app.service import BookService
from app.filter import admin_required
from app.forms import BookSearchForm,BookUpdateForm,SectionAddForm,UnitAddForm,SectionAddForm
from app.settings import Config

from flask_login import login_required
from flask import request,render_template,redirect,url_for,flash

from . import bp
import json
import base64

#书籍管理主页面
@bp.route('/book-manage/',methods=['GET','POST'])
@bp.route('/book-manage/<int:page>',methods=['GET','POST'])
@bp.route('/book-manage/<int:page>/values/<string:values>',methods=['GET','POST'])
@login_required
@admin_required
def book_manage(page=1,values=''):
    form = BookSearchForm()
    if request.method=='GET':
        values_json = {}
        if values != '':
            values_json = json.loads(base64.b64decode(values))
        pagination = BookService.search_bookinfo(values_json,page)
        return render_template('admin/book/book_manage.html',
                               form=form,
                               values = values,
                               book_list=pagination.items,
                               pagination=pagination,
                               active=Config.ADMIN_PAGE_ACTIVE['problem'])

    if form.validate_on_submit():
        values = base64.b64encode(json.dumps(form.to_dict()))
        return redirect(url_for('admin.book_manage', page=1, values=values))

    return redirect(url_for('admin.book_manage',page=page))

#添加书籍
@bp.route('/book-manage/add',methods=['GET','POST'])
@login_required
@admin_required
def book_add():
    form = BookUpdateForm()
    if request.method=='GET':
        return render_template('admin/book/book_add.html',
                               form=form,active=Config.ADMIN_PAGE_ACTIVE['problem'])

    if form.validate_on_submit():
        try:
            BookService.add_book(form)
            flash("Add book success","success")
        except:
            flash("Add book field","danger")

    return redirect(url_for('admin.book_manage'))

#书籍更新
@bp.route('/book-manage/book-update/<string:id>',methods=['GET','POST'])
@login_required
@admin_required
def book_update(id):
    form = BookUpdateForm()
    if request.method=='GET':
        book = BookService.get_book_by_id(id)
        form.book_name.data = book.book_name
        form.version.data = book.version
        form.author.data = book.author
        form.publisher.data = book.publisher
        form.publish_time.data = book.publish_time
        form.subject.data = book.subject
        return render_template('admin/book/book_update.html',
                               form=form,active=Config.ADMIN_PAGE_ACTIVE['problem'])

    if form.validate_on_submit():
        try:
            BookService.update_book(form,id)
            flash("Update book information success","success")
        except:
            flash("Update book infomation failed","danger")

    return render_template('admin/book/book_update.html',
                           form=form, active=Config.ADMIN_PAGE_ACTIVE['problem'])

#书籍目录更新
@bp.route('/book-manage/bookindex-update/<string:id>',methods=['GET','POST'])
@login_required
@admin_required
def bookindex_update(id):
    formUnit = UnitAddForm()
    formSection = SectionAddForm()
    #该书若不存在直接禁止访问此页面
    bookIsExist = BookService.get_book_by_id(id)
    if bookIsExist is None:
        return redirect(url_for('admin.book_manage'))

    if request.method=='GET':
        unit_list = BookService.get_unit_by_book(id)    #获取该书的所有章
        List = []           #该书所有章节总列表,列表每项为一个字典包含两个键unit,section
                            #unit下只有一个unit对象,section下为一个列表,列表每一项为一个section对象

        uid_list = []       #章id列表
        uname_list = []     #章名称列表
        key = ['unit', 'section']

        #遍历每一章，获取每一章对应的所有节存入value列表
        for unit in unit_list:
            uid_list.append(unit.unit_id)
            uname_list.append(unit.unit_name)
            value=[unit,BookService.get_section_by_unit(unit.unit_id)]
            List.append(dict(zip(key,value)))

        formUnit.bookid.data = id
        #为右边工具栏“节添加”操作的select赋值
        formSection.unitid.choices = zip(uid_list,uname_list)
        return render_template('admin/book/book_index_update.html',
                               List=List,
                               formUnit=formUnit,
                               formSection=formSection,
                               book_id=id,
                               active=Config.ADMIN_PAGE_ACTIVE['problem'])
    #章添加的表单合法性验证
    if formUnit.submitunit.data :
        unit = UnitInfo()
        unit.belong_to_book = formUnit.bookid.data
        unit.unit_name = formUnit.unitname.data
        BookService.add_unit(unit)
    #节添加的表单合法性验证
    if formSection.submitsection.data :
        section = SectionInfo()
        section.belong_to_unit = formSection.unitid.data
        section.section_name = formSection.sectionname.data
        BookService.add_section(section)
    #获取前端名为update_unit的input按钮的返回值,若有返回值则存在对应表单的操作
    if request.form.get('update_unit'):
        unit = UnitInfo()
        unit.unit_id = request.form.get('unit_id')
        unit.unit_name = request.form.get('unit_name')
        BookService.update_unit(unit)
    #获取前端名为update_section的input按钮的返回值,若有返回值则存在对应表单的操作
    if request.form.get('update_section'):
        section = SectionInfo()
        section.section_id = request.form.get('section_id')
        section.section_name = request.form.get('section_name')
        BookService.update_section(section)

    return redirect(url_for('admin.bookindex_update',id=id))

#书籍删除
@bp.route('/book-manage/delete/book/<string:id>')
@login_required
@admin_required
def book_delete(id):
    try:
        BookService.delete_book(id)
        flash(u"已成功删除书籍",'success')
    except:
        flash(u'删除书籍失败,请检查日志','danger')
    return redirect(url_for('admin.book_manage'))
#章和节的删除
@bp.route('/book-manage/<string:book_id>/delete/<string:type>/<string:id>')
@login_required
@admin_required
def index_delete(book_id,type,id):

    try:
        if type == 'section':
            BookService.delete_section(id)
        if type == 'unit':
            BookService.delete_unit(id)
        flash(u'成功删除章/节','success')
    except:
        flash(u'删除章/节失败,请检查日志','danger')
    return redirect(url_for('admin.bookindex_update',id=book_id))