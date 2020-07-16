import os
import uuid
import json
from pathlib import Path
from flask import current_app, render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from werkzeug.utils import secure_filename



bp = Blueprint('urlshort', __name__)

@bp.record
def record_params(setup_state):
    global db
    db = setup_state.app.config['db']


@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        
        code = db.urls.find_one({'code': request.form['code']})
        if code is not None:
            flash('That name is already being selected. Please choose another one!')
            return redirect(url_for('urlshort.home'))

        urls['code'] = request.form['code']
        if 'url' in request.form.keys():
            urls['data'] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = str(uuid.uuid4()) + secure_filename(f.filename)

            # ref: http://zetcode.com/python/pathlib/
            full_path = Path.cwd() / 'urlshort' / 'static' / 'users_files' / full_name

            f.save(full_path)
            urls['data'] = {'file': full_name}

        # Saving url in mongo collection
        db.urls.insert(urls)

        # storing users data in session/cookies
        session[request.form['code']] = True

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirect_to_url(code):
    url = db.urls.find_one({'code': code})
    if url is not None:
        if 'url' in url['data'].keys():
            return redirect(url['data']['url'])
        else:
            return redirect(url_for('static', filename='users_files/'+url['data']['file']))
    return abort(404)


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
