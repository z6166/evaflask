# -*- coding=utf-8 -*-
from . import admin
from flask import render_template, flash, redirect, url_for, request, jsonify, send_from_directory, abort
from flask_login import login_required, current_user, login_user, logout_user
from forms import EditArticleForm,EditCategoryForm,PostArticleForm,PostCategoryForm,EditCommentForm,LoginForm, RegistrationForm, EditRecordForm, ModifyForm, EditErecordForm
from ..models import User, Record,Erecord,Comment,Article,Category
from .. import db
from datetime import datetime
from xlwt import *
import os

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.record'))
        flash(u'用户密码不正确')
    return render_template('admin/login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    register_key = 'zhucema'
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.registerkey.data != register_key:
            flash(u'注册码不符，请返回重试')
            return redirect(url_for('admin.register'))
        else:
            if form.password.data != form.password2.data:
                flash(u'两次输入密码不一')
                return redirect(url_for('admin.register'))
            else:
                try:
                    user = User(username=form.username.data, password=form.password.data)
                    db.session.add(user)
                    db.session.commit()
                    flash(u'您已经成功注册')
                    return redirect(url_for('admin.login'))
                except:
                    db.session.rollback()
                    flash(u'用户名已存在')
    return render_template('admin/register.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经登出了系统')
    return redirect(url_for('admin.index'))


@admin.route('/record', methods=['GET', 'POST'])
@login_required
def record():
    status = request.args.get('status')
    allnum=db.session.query(Record).count()
    nsolvenum=db.session.query(Record).filter(Record.solve == False).count()
    nverifynum=db.session.query(Record).filter(Record.verify == False).count()
    oknum=db.session.query(Record).filter(Record.verify == True).filter(Record.mender!= '').filter(Record.solve == True).count()
    nobody=db.session.query(Record).filter(Record.mender == '').count()
    print status
    if status=='2':
        results = db.session.query(Record).filter(Record.verify == False).order_by(-Record.id)
    elif status=='3':
        results = db.session.query(Record).filter(Record.solve == False).order_by(-Record.id)
    elif status=='4':
        results = db.session.query(Record).filter(Record.verify == True).filter(Record.mender != '').filter(Record.solve == True).order_by(-Record.id)
    elif status=='5':
        results = db.session.query(Record).filter(Record.mender == '').order_by(-Record.id)
    else:
        results = db.session.query(Record).order_by(-Record.id)
    form = ModifyForm()
    if form.validate_on_submit():
        return redirect(url_for('admin.modify', id=form.id.data))
    return render_template('admin/record.html', results=results, form=form ,nsolvenum=nsolvenum, nverifynum=nverifynum, oknum=oknum, allnum=allnum, nobody=nobody)

@admin.route('/erecord', methods=['GET', 'POST'])
@login_required
def erecord():
    status = request.args.get('status')
    allnum=db.session.query(Erecord).count()
    nsolvenum=db.session.query(Erecord).filter(Erecord.solve == False).count()
    nverifynum=db.session.query(Erecord).filter(Erecord.verify == False).count()
    oknum=db.session.query(Erecord).filter(Erecord.verify == True).filter(Erecord.mender!= '').filter(Erecord.solve == True).count()
    nobody = db.session.query(Erecord).filter(Erecord.mender == '').count()
    print status
    if status=='2':
        results = db.session.query(Erecord).filter(Erecord.verify == False).order_by(-Erecord.id)
    elif status=='3':
        results = db.session.query(Erecord).filter(Erecord.solve == False).order_by(-Erecord.id)
    elif status=='4':
        results = db.session.query(Erecord).filter(Erecord.verify == True).filter(Erecord.mender!= '').filter(Erecord.solve == True).order_by(-Erecord.id)
    elif status=='5':
        results = db.session.query(Erecord).filter(Erecord.mender == '').order_by(-Erecord.id)
    else:
        results = db.session.query(Erecord).order_by(-Erecord.id)
    form = ModifyForm()
    if form.validate_on_submit():
        return redirect(url_for('admin.emodify', id=form.id.data))
    return render_template('admin/erecord.html', results=results, form=form ,nsolvenum=nsolvenum, nverifynum=nverifynum, oknum=oknum, allnum=allnum,nobody=nobody)

@admin.route('/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify(id):
    re = db.session.query(Record).filter(Record.id == id).one()
    form = EditRecordForm(user=re.user, phone=re.phone, problem=re.problem, computer_type=re.computer_type,
                          computer_password=re.computer_password, split=re.split, solve=re.solve, mender=re.mender,
                          verify=re.verify)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            cord = Record.query.get_or_404(id)
            try:
                db.session.delete(cord)
                db.session.commit()
                return redirect(url_for('admin.record'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.modify', id=id))
        elif form.delete.data == "":
            cord = Record.query.get_or_404(id)
            cord.user = form.user.data
            cord.phone = form.phone.data
            cord.problem = form.problem.data
            cord.computer_type = form.computer_type.data
            cord.computer_password = form.computer_password.data
            cord.mender = form.mender.data
            if form.split.data:
                cord.split = True
            else:
                cord.split = False
            if form.solve.data:
                cord.solve = True
            else:
                cord.solve = False
            if form.verify.data:
                cord.verify = True
            else:
                cord.verify = False
            try:
                db.session.add(cord)
                db.session.commit()
                return redirect(url_for('admin.record'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.modify', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.modify', id=id))
    return render_template("admin/modify.html", form=form, id=re.id, time=re.create_time, random_id=re.random_id)

@admin.route('/emodify/<int:id>', methods=['GET', 'POST'])
@login_required
def emodify(id):
    re = db.session.query(Erecord).filter(Erecord.id == id).one()
    form = EditErecordForm(user=re.user, phone=re.phone, problem=re.problem, ele_type=re.ele_type, solve=re.solve, mender=re.mender,
                          verify=re.verify)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            cord = Erecord.query.get_or_404(id)
            try:
                db.session.delete(cord)
                db.session.commit()
                return redirect(url_for('admin.erecord'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.emodify', id=id))
        elif form.delete.data == "":
            cord = Erecord.query.get_or_404(id)
            cord.user = form.user.data
            cord.phone = form.phone.data
            cord.problem = form.problem.data
            cord.ele_type = form.ele_type.data
            cord.mender = form.mender.data
            if form.solve.data:
                cord.solve = True
            else:
                cord.solve = False
            if form.verify.data:
                cord.verify = True
            else:
                cord.verify = False
            try:
                db.session.add(cord)
                db.session.commit()
                return redirect(url_for('admin.erecord'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.emodify', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.emodify', id=id))
    return render_template("admin/emodify.html", form=form, id=re.id, time=re.create_time, random_id=re.random_id)


@admin.route('/download', methods=['GET', 'POST'])
@login_required
def download():
    results = db.session.query(Record).order_by(-Record.id)
    w = Workbook(encoding='utf-8')
    ws = w.add_sheet('record')
    ws.write(0, 0, "序号")
    ws.write(0, 1, "登记时间")
    ws.write(0, 2, "随机码")
    ws.write(0, 3, "送修者姓名")
    ws.write(0, 4, "联系方式")
    ws.write(0, 5, "故障")
    ws.write(0, 6, "机型")
    ws.write(0, 7, "是否拆机")
    ws.write(0, 8, "是否解决")
    ws.write(0, 9, "是否取回")
    ws.write(0, 10, "维修者")
    x = 1
    for re in results:
        ws.write(x, 0, re.id)
        ws.write(x, 1, re.create_time)
        ws.write(x, 2, re.random_id)
        ws.write(x, 3, re.user)
        ws.write(x, 4, re.phone)
        ws.write(x, 5, re.problem)
        ws.write(x, 6, re.computer_type)
        ws.write(x, 7, re.split)
        ws.write(x, 8, re.solve)
        ws.write(x, 9, re.verify)
        ws.write(x, 10, re.mender)
        x += 1
    w.save('computerrecord.xls')
    # os.system("rm app/static/admin/record.xls")
    os.system("mv computerrecord.xls app/static/admin/")
    # return send_from_directory("upload","/app/admin/static/record.xls", as_attachment=True)
    eresults = db.session.query(Erecord).order_by(-Erecord.id)
    w = Workbook(encoding='utf-8')
    ws = w.add_sheet('erecord')
    ws.write(0, 0, "序号")
    ws.write(0, 1, "登记时间")
    ws.write(0, 2, "随机码")
    ws.write(0, 3, "送修者姓名")
    ws.write(0, 4, "联系方式")
    ws.write(0, 5, "故障")
    ws.write(0, 6, "类型")
    ws.write(0, 7, "是否解决")
    ws.write(0, 8, "是否取回")
    ws.write(0, 9, "维修者")
    x = 1
    for re in eresults:
        Thetime = re.create_time.strftime("%Y-%m-%d %H:%M:%S")
        ws.write(x, 0, re.id)
        ws.write(x, 1, Thetime)
        ws.write(x, 2, re.random_id)
        ws.write(x, 3, re.user)
        ws.write(x, 4, re.phone)
        ws.write(x, 5, re.problem)
        ws.write(x, 6, re.ele_type)
        ws.write(x, 7, re.solve)
        ws.write(x, 8, re.verify)
        ws.write(x, 9, re.mender)
        x += 1
    w.save('elerecord.xls')
    # os.system("rm app/static/admin/record.xls")
    os.system("mv elerecord.xls app/static/admin/")
    # return send_from_directory("upload","/app/admin/static/record.xls", as_attachment=True)
    return render_template("admin/download.html")

@admin.route('/comment', methods=['GET', 'POST'])
@login_required
def comment():
    comment = db.session.query(Comment).order_by(-Comment.id)
    form = ModifyForm()
    if form.validate_on_submit():
        return redirect(url_for('admin.commentmodify', id=form.id.data))
    return render_template('admin/comment.html', form=form,comment=comment)


@admin.route('/commentmodify/<int:id>', methods=['GET', 'POST'])
@login_required
def commentmodify(id):
    co = db.session.query(Comment).filter(Comment.id == id).one()
    form = EditCommentForm(comment=co.comment,verify=co.verify)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            cord = Comment.query.get_or_404(id)
            try:
                db.session.delete(cord)
                db.session.commit()
                return redirect(url_for('admin.comment'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.commentmodify', id=id))
        elif form.delete.data == "":
            cord = Comment.query.get_or_404(id)
            cord.comment = form.comment.data
            if form.verify.data:
                cord.verify = True
            else:
                cord.verify = False
            try:
                db.session.add(cord)
                db.session.commit()
                return redirect(url_for('admin.comment'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.commentmodify', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.commentmodify', id=id))
    return render_template("admin/commentmodify.html", form=form, id=co.id)

@admin.route('/category', methods=['GET', 'POST'])
def category():
    clist = Category.query.all()
    form = PostCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        flash(u'分类添加成功')
        return redirect(url_for('admin.index'))
    return render_template('admin/category.html', form=form, list=clist)

@admin.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def category_edit(id):
    ca = db.session.query(Category).filter(Category.id == id).one()
    form = EditCategoryForm(name=ca.name)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            dca = Category.query.get_or_404(id)
            try:
                db.session.delete(dca)
                db.session.commit()
                return redirect(url_for('admin.category'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.category_edit', id=id))
        elif form.delete.data == "":
            dca = Category.query.get_or_404(id)
            dca.name = form.name.data
            try:
                db.session.add(dca)
                db.session.commit()
                return redirect(url_for('admin.category'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.category_edit', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.category_edit', id=id))
    return render_template("admin/category_edit.html", form=form, id=ca.id)

@admin.route('/trouble', methods=['GET', 'POST'])
@login_required
def article():
    form = PostArticleForm()
    alist = Article.query.all()
    if form.validate_on_submit():
        acticle = Article(title=form.title.data, body=form.body.data, category_id=str(form.category_id.data.id),
                          user_id=current_user.id)
        db.session.add(acticle)
        flash(u'文章添加成功')
        return redirect(url_for('admin.index'))
    return render_template('admin/article.html', form=form, list=alist)

@admin.route('/trouble/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def article_edit(id):
    ar = db.session.query(Article).filter(Article.id == id).one()
    form = EditArticleForm(title=ar.title,body=ar.body,category_id=ar.category_id)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            dar = Article.query.get_or_404(id)
            try:
                db.session.delete(dar)
                db.session.commit()
                return redirect(url_for('admin.article'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.article_edit', id=id))
        elif form.delete.data == "":
            dar = Article.query.get_or_404(id)
            dar.title = form.title.data
            dar.body = form.body.data
            dar.category_id=str(form.category_id.data.id)
            try:
                db.session.add(dar)
                db.session.commit()
                return redirect(url_for('admin.article'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.article_edit', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.article_edit', id=id))
    return render_template("admin/article_edit.html", form=form, id=ar.id)
