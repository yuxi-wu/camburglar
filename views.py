from flask import render_template, request
from app import app
from form import UrlForm
from anti_sensor import sensing

@app.route("/model")
@app.route('/')
def homepage():
    print('routed correctly')
    form = UrlForm()
    return render_template('home.html',
                           title="Hamburglar!",
                           form=form)

@app.route("/results.html", methods=["post"])
def results():
    try:
        results = sense(int(request.form['Length']), int(request.form['Width']))
        results = {'results': pd.DataFrame(results).to_html()}

    except AssertionError:
        results = {'none': ['']}

    return render_template("results.html", data=results)
