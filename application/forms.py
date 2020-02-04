# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class RequestForm(FlaskForm):
    body = StringField('Введите ваш отчёт об ошибке: ', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class ResponseForm(FlaskForm):
    body = TextAreaField('Ваш отчёт относится к: ', widget=TextArea())
