# -*- coding=utf-8 -*-
from flask_wtf import FlaskForm
# from ..models import
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required, length, Regexp, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.pagedown.fields import PageDownField
from ..models import Category


class LoginForm(FlaskForm):
    username = StringField(u'帐号', validators=[Required(), length(6, 18)])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登入')


class RegistrationForm(FlaskForm):
    username = StringField(u'用户名', validators=[Required(), length(6, 18), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只允许字母')])
    password = PasswordField(
        u'密码', validators=[Required(), EqualTo('password2', message=u'两次密码不一致')])
    password2 = PasswordField(u'重复密码', validators=[Required()])
    # real_name = StringField(u'昵称', validators=[Required()])
    registerkey = StringField(u'注册码', validators=[Required()])
    submit = SubmitField(u'注册')


class EditRecordForm(FlaskForm):
    user = StringField(u'* 物主姓名:', validators=[Required(), length(2, 5, message=u'姓名只允许2-5个字！')])
    phone = StringField(u'* 手机号或QQ号:', validators=[Required(), length(6, 11, message=u'只允许6-11位数字'), Regexp('[0-9]')])
    problem = TextAreaField(u'* 故障介绍:', validators=[Required()])
    computer_type = StringField(u'* 电脑型号:', validators=[Required()])
    computer_password = StringField(u'电脑密码（可不填）:')
    split = BooleanField(u'* 拆机请打钩')
    solve = BooleanField(u'* 已解决请打钩')
    verify = BooleanField(u'* 已取回请打钩')
    mender = StringField(u'* 维修者姓名：')
    delete = StringField(u'如果你要删除这条记录，输入“确认删除”之后点击提交！否则请留空。')
    submit = SubmitField(u'提交')

class EditErecordForm(FlaskForm):
    user = StringField(u'* 物主姓名:', validators=[Required(), length(2, 5, message=u'姓名只允许2-5个字！')])
    phone = StringField(u'* 手机号或QQ号:', validators=[Required(), length(6, 11, message=u'只允许6-11位数字'), Regexp('[0-9]')])
    problem = TextAreaField(u'* 故障介绍:', validators=[Required()])
    ele_type = StringField(u'* 电器类型:', validators=[Required()])
    solve = BooleanField(u'* 已解决请打钩')
    verify = BooleanField(u'* 已取回请打钩')
    mender = StringField(u'* 维修者姓名：')
    delete = StringField(u'如果你要删除这条记录，输入“确认删除”之后点击提交！否则请留空。')
    submit = SubmitField(u'提交')

class ModifyForm(FlaskForm):
    id = StringField(u'id')
    submit = SubmitField(u'修改')

class EditCommentForm(FlaskForm):
    comment = TextAreaField(u'更改评论为:', validators=[Required()])
    verify = BooleanField(u'加精请打勾')
    delete = StringField(u'如果你要删除这条记录，输入“确认删除”之后点击提交！否则请留空。')
    submit = SubmitField(u'提交')

class EditArticleForm(FlaskForm):
    title = TextAreaField(u'更改标题为:', validators=[Required()])
    body = PageDownField(u'更改内容为:', validators=[Required()])
    category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(
    ), get_pk=lambda a: str(a.id), get_label=lambda a: a.name)
    delete = StringField(u'如果你要删除这条记录，输入“确认删除”之后点击提交！否则请留空。')
    submit = SubmitField(u'提交')

class EditCategoryForm(FlaskForm):
    name = TextAreaField(u'更改名字为:', validators=[Required()])
    delete = StringField(u'如果你要删除这条记录，输入“确认删除”之后点击提交！否则请留空。')
    submit = SubmitField(u'提交')

class PostArticleForm(FlaskForm):
    title = StringField(u'标题', validators=[Required(), length(1, 64)])
    body = PageDownField(u'内容')
    category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(
    ), get_pk=lambda a: str(a.id), get_label=lambda a: a.name)
    submit = SubmitField(u'发布')

class PostCategoryForm(FlaskForm):
    name = StringField(u'分类名', validators=[Required(), length(1, 64)])
    submit = SubmitField(u'发布')