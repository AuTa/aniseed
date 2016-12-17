# coding: utf-8

from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.fields.html5 import URLField, DateTimeField
from wtforms.validators import DataRequired, URL
from wtforms import ValidationError


class QiniuAuthForm(Form):
    access_key = StringField('access_key')
    secret_key = StringField('secret_key')
    qiniu_auth = SubmitField('提交')


class ProjectInfoForm(Form):
    project_name = StringField('项目名称')
    project_address = StringField('项目地址')
    project_info = TextAreaField('项目介绍')
    project_name_en = StringField('项目名称en')
    project_address_en = StringField('项目地址en')
    project_info_en = TextAreaField('项目介绍en')
    project_time = StringField('项目时间')
    project_info_submit = SubmitField('确认')
