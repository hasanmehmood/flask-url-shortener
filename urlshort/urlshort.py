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
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        
        if request.form['code'] in urls.keys():
            flash('That name is already being selected. Please choose another one!')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = str(uuid.uuid4()) + secure_filename(f.filename)

            # ref: http://zetcode.com/python/pathlib/
            full_path = Path.cwd() / 'urlshort' / 'static' / 'users_files' / full_name

            f.save(full_path)
            urls[request.form['code']] = {'file': full_name}

        # Saving urls dict in a json file
        with open('urls.json', 'w') as urls_file:
            json.dump(urls, urls_file)

            # storing users data in session/cookies
            session[request.form['code']] = True

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='users_files/'+urls[code]['file']))
    
    return abort(404)


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
