from flask import Flask
from os import urandom

app = Flask(__name__)

from views import *


app.config["WTF_CSRF_ENABLED"] = True
app.config["SECRET_KEY"] = urandom(24)

if __name__ == '__main__':
    app.run(port=5001)
