from flask import render_template, redirect, url_for
from application import app
from application.forms import RequestForm, ResponseForm
from application.model import Model


@app.route('/')
def index():
    return redirect(url_for('submit'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    request_form = RequestForm()
    if request_form.validate_on_submit():
        Model.send_report(request_form.body.data)
        return redirect(url_for('response'))
    return render_template('submit.html', form=request_form)


@app.route('/response', methods=['GET'])
def response():
    response_form = ResponseForm()
    response_form.body.data = Model.get_response()
    return render_template('response.html', form=response_form)
