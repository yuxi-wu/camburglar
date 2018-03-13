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
        num_dev, table = sense(int(request.form['Length']), int(request.form['Width']))

        results = {'results':num_dev}

    except AssertionError:
        results = {'none': ['']}

    return render_template("results.html", tables=[table], data=results)
