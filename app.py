import os
import uuid
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'somethingveryrandom'

@app.route('/')
def home():
    return render_template('home.html', name='Hassan')


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        
        if request.form['code'] in urls.keys():
            flash('That name is already being selected. Please choose another one!')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = str(uuid.uuid4()) + secure_filename(f.filename)
            full_path = Path.cwd() / 'file_uploads' / full_name
            f.save(full_path)
            urls[request.form['code']] = {'file': full_name}

        # Saving urls dict in a json file
        with open('urls.json', 'w') as urls_file:
            json.dump(urls, urls_file)

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))