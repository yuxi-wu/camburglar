from flask import render_template, request
from app import app
from form import UrlForm
from anti-sensor import traffic, localization

@app.route("/model")
@app.route('/')
def homepage():
    print('routed correctly')
    form = UrlForm()
    return render_template('index.html',
                           title="Hamburglar!",
                           form=form)

@app.route("/results", methods=["post"])
def results():
    '''
    try:
        data = predictor_chi(request.form['Length'],\
            request.form['Width'])
    except AssertionError:
        data = {'none': ['']}
    return render_template("wp_results.html", data=data)
    '''
