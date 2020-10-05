from muzzle import app
from flask import render_template, url_for, flash, request


@app.route('/')
def index():
    return render_template('index.html', links=app.config['ALL_LINKS'])


@app.route('/test', methods=['post', 'get'])
def test():
    return render_template('test.html')
