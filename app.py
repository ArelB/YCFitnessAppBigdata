from flask import Flask
from flask_cors import CORS, cross_origin

import Felix
import Wouter
import WeerApi
import VoortgangVisualisatie
import RunTipsScraping

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#TESTPAGINAS
#placeholder home pagina, niet meer nodig als backend online staat
@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!!</p>"
#test pagina: print iets
@app.route("/tweede")
def Felixfunctie():
    return Felix.vanFelix1()
#test pagina: csv bestand uitlezen
@app.route("/csv")
def csv():
    return Wouter.csvFunctie()
#test pagina: return basic columns met stijl can html bestand
@app.route("/csvMetStijl")
def csvStijl():
    return Wouter.csvStijl()
#test pagina: return basic colomns in json format
@app.route("/csvJSON")
@cross_origin()
def csvJSON():
    return Wouter.csvJSON()
#test pagina: return met input van adress
@app.route("/csv/<pok>")
def printpok(pok):
    return Wouter.printPokemon(pok)
#test pagina: azuredatabase connectie
@app.route("/testdbcon")
def dbconnectie():
    return Wouter.azuredatabaseconnectie()
#connectie met persoonlijkedatabase en voortgang van route visualiseren
@app.route("/VoortgangVisualPDB")
def printpersonalGraph():
    return Wouter.ShowGraph()




#BELANGRIJKE APP PAGINAS
#download laatste weer data van api
@app.route("/apiCall")
def callapi():
    return WeerApi.homepagina()

#choose locatie van weer
@app.route("/apiWeer")
def printhomeweer():
    return WeerApi.homepagina()

#return weer van locatie
@app.route("/apiWeer/<loc>")
def printweer(loc):
    return WeerApi.NCdata(loc)   

#pagina die aangeeft dat je een persoon moet kiezen
@app.route("/VoortgangVisual")
def printhomevisual():
    return "Kies een persoon door '/' met de naam van een persoon achter de url te typen en op enter te klikken"

#connectie met database en voortgang van route visualiseren voor een persoon
@app.route("/VoortgangVisual/<persoon>")
def printGraph(persoon):
    return VoortgangVisualisatie.ShowGraph(persoon)

#data scrapen van website en random tip tonen
@app.route("/RunTip")
def printRunTip():
    return RunTipsScraping.GetTip()

#voor niet flask refreshen, run python app.py met hieronder niet in commentaar
#app.run(debug=True)
