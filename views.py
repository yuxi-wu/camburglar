from flask import render_template, request
from app import app
from form import UrlForm
from anti_sensor.sensing import sense

@app.route("/anti")
@app.route('/')
def homepage():
    print('routed correctly')
    form = UrlForm()
    return render_template('home.html',
                           title="Hamburglar!",
                           form=form)

#@app.route('')
@app.route("/results", methods=["post"])
def results():
    try:
        results = {'results': sense(int(request.form['Length']), int(request.form['Width']))}

    except AssertionError:
        results = {'none': ['']}

    return render_template("results.html", data=results)
