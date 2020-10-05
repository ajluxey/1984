from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    image = FileField('Образ')
    config = FileField('Конфиг')
    description = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Загрузить')
