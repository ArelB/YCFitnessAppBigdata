from flask import Flask
import Felix

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!!</p>"

@app.route("/tweede")
def andere():
    return Felix.vanFelix1()