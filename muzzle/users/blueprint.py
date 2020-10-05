from flask import Blueprint
from flask import render_template
from muzzle import app

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@users.route('/')
def usr_index():
    return render_template('user_index.html', links=app.config['ALL_LINKS'])


@users.route('/login', methods=['post', 'get'])
def login():
    return render_template('login.html', links=app.config['ALL_LINKS'])


@users.route('/registration', methods=['post', 'get'])
def registration():
    return render_template('registration.html', links=app.config['ALL_LINKS'])