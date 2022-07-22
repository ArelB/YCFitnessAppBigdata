from flask import Flask
from flask import render_template
import Felix
import Wouter

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!!</p>"

@app.route("/tweede")
def andere():
    return Felix.vanFelix1()

@app.route("/csv")
def nieuw():
    return Wouter.csvFunctie()

@app.route("/csv/<pok>")
def printpok(pok):
    return Wouter.printPokemon(pok)