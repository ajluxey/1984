from flask import Flask, url_for
from muzzle import config

app = Flask(__name__)
app.config.update(config.flask_config)
# app.add_url_rule('/favicon.ico', redirect_to=url_for('static/img', filename=''))

from muzzle import view
from muzzle.images.blueprint import images
from muzzle.users.blueprint import users

app.register_blueprint(images, url_prefix='/images')
app.register_blueprint(users, url_prefix='/users')
app.run(host=app.config['HOST'], port=app.config['PORT'])
