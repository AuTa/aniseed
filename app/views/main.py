# coding: utf-8
import codecs

from flask import Blueprint, render_template, redirect, url_for, request, flash, session, \
    jsonify, make_response, abort
from datetime import timedelta, datetime
import time
import hashlib
import json
from copy import deepcopy
from qiniu import Auth
from app.forms import QiniuAuthForm, ProjectInfoForm

Project = {'project_name': '',
           'project_name_en': '',
           'project_address': '',
           'project_address_en': '',
           'project_time':'',
           'project_info': '',
           'project_info_en': '',
           'background_url': '',
           'project_url': [],
           'background_color': False
           }

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index(id=None):
    with open('./data.json', 'r') as f:
        try:
            data = json.load(f)
        except:
            data = {'Project': []}
    if session.get('qiniu_auth') is None:
        with open('./qiniu.json', 'r') as f:
            try:
                qiniu_auth = json.load(f)
            except:
                qiniu_auth = {'access_key':'', 'secret_key':''}
        session['qiniu_auth'] = qiniu_auth
    qiniu_auth_form = QiniuAuthForm()

    project = data['Project']
    project.append(Project)

    if qiniu_auth_form.validate_on_submit():
        session['qiniu_auth']['access_key'] = qiniu_auth_form.access_key.data
        session['qiniu_auth']['secret_key'] = qiniu_auth_form.secret_key.data
        with open('./qiniu.json', 'w') as f:
            json.dump(session.get('qiniu_auth'), f)
        return redirect(url_for('.index'))

    qiniu_auth_form.access_key.data = session.get('qiniu_auth')['access_key']
    qiniu_auth_form.secret_key.data = session.get('qiniu_auth')['secret_key']

    return render_template('index.html',
                           form=qiniu_auth_form,
                           qiniu=session.get('qiniu_auth'),
                           project=project)


@main.route('/<int:id>', methods=['GET', 'POST'])
def project(id):
    with codecs.open('./data.json', 'r', 'utf-8') as f:
        try:
            data = json.load(f)
        except:
            data = {'Project': []}

    if session.get('qiniu_auth') is None:
        with open('./qiniu.json', 'r') as f:
            try:
                qiniu_auth = json.load(f)
            except:
                qiniu_auth = {'access_key':'', 'secret_key':''}
        session['qiniu_auth'] = qiniu_auth

    project_info_form = ProjectInfoForm()

    project = data['Project']
    project.append(Project)

    if project_info_form.validate_on_submit():
        project_info = project[id-1]
        project_info['project_name'] = project_info_form.project_name.data
        project_info['project_address'] = project_info_form.project_address.data
        project_info['project_info'] = project_info_form.project_info.data
        project_info['project_name_en'] = project_info_form.project_name_en.data
        project_info['project_address_en'] = project_info_form.project_address_en.data
        project_info['project_info_en'] = project_info_form.project_info_en.data
        project_info['project_time'] = project_info_form.project_time.data

        if id != len(project):
            project.pop()

        with codecs.open('./data.json', 'w', "utf-8") as f:
            s = json.dumps(data, ensure_ascii=False)
            f.write(s)

        return redirect(url_for('.project', id=id))

    if project[id-1]:
        project_info_form.project_name.data = project[id-1]['project_name']
        project_info_form.project_address.data = project[id-1]['project_address']
        project_info_form.project_info.data = project[id-1]['project_info']
        project_info_form.project_name_en.data = project[id-1]['project_name_en']
        project_info_form.project_address_en.data = project[id-1]['project_address_en']
        project_info_form.project_info_en.data = project[id-1]['project_info_en']
        project_info_form.project_time.data = project[id-1]['project_time']
    else:
        abort(404)
    return render_template('project.html',
                           form=project_info_form,
                           project=project,
                           id=id)

@main.route('/uptoken', methods=['POST'])
def uptoken():
    q = Auth(session.get('qiniu_auth')['access_key'], session.get('qiniu_auth')['secret_key'])
    token = q.upload_token('dl-atelier')

    return jsonify(uptoken=token)
