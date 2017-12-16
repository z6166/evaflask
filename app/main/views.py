#-*- coding=utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from . import main
from .forms import AddCommentForm,AddComRecordForm, GetRandomIdForm,AddEleRecordForm,PostInquire
from ..models import Record,Erecord,Unid,Comment,Article,Category
from .. import db
from datetime import datetime
import random
import string


@main.route('/')
def index():
    '''
    clist = Category.query.all()
    alist = Article.query.all()
    return render_template('main/index.html',clist=clist,alist=alist)
    '''
    return redirect(url_for('main.user_amend'))


@main.route('/.well-known/pki-validation/fileauth.txt')
def tencentssl():
    return '201712101454112neoivuld5m1usydql34l0sudhgrsq8g6hmmqxko2xs3nvkuxh'

@main.route('/user/amend', methods=['GET', 'POST'])
def user_amend():
    """
    用户添加维修记录
    :return:
    """
    dayOfWeek = datetime.today().weekday()
    type = request.args.get('type')
    if type == '2':
        form = AddEleRecordForm()
    else:
        form = AddComRecordForm()
    # alist = Record.query.all()
    if form.validate_on_submit():
        unid = Unid(random_id = string.join(
            random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5)).replace(' ', ''))
        try:
            db.session.add(unid)
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'随机码生成失败')
        if type == '2':
            erecord = Erecord(user=form.user.data, phone=form.phone.data, problem=form.problem.data,
                              create_time=datetime.now(), ele_type=form.ele_type.data, random_id=unid.random_id)
        else:
            record = Record(user=form.user.data, phone=form.phone.data, problem=form.problem.data,
                            create_time=datetime.now(),
                            computer_type=form.computer_type.data, computer_password=form.computer_password.data,
                            random_id=unid.random_id)
        i = 1
        while(i):
            try:
                if type == '2':
                    db.session.add(erecord)
                    db.session.commit()
                    flash(u'记录添加成功,您的随机码是 %s, 请务必截图保存' % erecord.random_id)
                else:
                    db.session.add(record)
                    db.session.commit()
                    flash(u'记录添加成功,您的随机码是 %s, 请务必截图保存' % record.random_id)
                i = 0
                return redirect(url_for('main.user_verify', random_id=unid.random_id))
            except:
                db.session.rollback()
    return render_template('main/amend.html', form=form)


@main.route('/user/verify/<int:random_id>', methods=['GET', 'POST'])
def user_verify(random_id):
    """
    用户确认物品取回
    :return:
    """
    form = GetRandomIdForm(random_id=random_id)
    if form.validate_on_submit():
        random_id = form.random_id.data
        record = Record.query.filter(Record.random_id == random_id).first()
        if record is None:
            erecord = Erecord.query.filter(Erecord.random_id == random_id).first()
            erecord.verify = True
            db.session.add(erecord)
            db.session.commit()
            flash(u'已确认取回')
        else:
            try:
                record.verify = True
                db.session.add(record)
                db.session.commit()
                flash(u'已确认取回')
            except:
                db.session.rollback()
                flash(u'未知错误')
        return redirect(url_for('main.user_amend'))
    return render_template('main/verify.html', form=form)


@main.route('/user/verify', methods=['GET', 'POST'])
def user_Verify():
    """
    用户确认物品取回
    :return:
    """
    form = GetRandomIdForm()
    if form.validate_on_submit():
        random_id = form.random_id.data
        record = Record.query.filter(Record.random_id == random_id).first()
        if record is None:
            erecord = Erecord.query.filter(Erecord.random_id == random_id).first()
            erecord.verify = True
            db.session.add(erecord)
            db.session.commit()
            flash(u'已确认取回')
        else:
            try:
                record.verify = True
                db.session.add(record)
                db.session.commit()
                flash(u'已确认取回')
            except:
                db.session.rollback()
                flash(u'未知错误')
        return redirect(url_for('main.user_amend'))
    return render_template('main/verify.html', form=form)

@main.route('/comment', methods=['GET', 'POST'])
def comment():
    form = AddCommentForm()
    if form.validate_on_submit():
        comment = Comment(comment = form.comment.data,create_time=datetime.now())
        i = 1
        while(i):
            try:
                db.session.add(comment)
                db.session.commit()
                flash(u'评论提交成功')
                i = 0
                return redirect(url_for('main.index'))
            except:
                db.session.rollback()
    return render_template('main/comment.html', form=form)

@main.route('/read/', methods=['GET'])
def read():
    a = Article.query.filter_by(id=request.args.get('id')).first()
    if a is not None:
        return render_template('main/read.html', a=a)
    flash(u'未找到相关文章')
    return redirect(url_for('main.index'))


@main.route('/user/inquire/', methods=['GET', 'POST'])
def inquire():
    form = PostInquire()
    if form.validate_on_submit():
        random_id = form.random_id.data
        record = Record.query.filter(Record.random_id == random_id).first()
        if record is None:
            record = Erecord.query.filter(Erecord.random_id == random_id).first()
        if record is None:
            flash(u'登记码错误')
        else:
            status = record.solve
            return render_template('main/inquire.html', form=form, status=status)
    return render_template('main/inquire.html', form=form)

