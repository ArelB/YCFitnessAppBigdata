import pandas
from flask import render_template
import json
import requests
from pathlib import Path
from netCDF4 import Dataset
import datetime
import pyodbc as odbc


#lees een csv bestand in repo
def csvFunctie():
    df = pandas.read_csv("Pokemon.csv")
    return str(df.columns)

#lees csv bestand gefilterd op argument
def printPokemon(pok):
    df = pandas.read_csv("Pokemon.csv") 
    return pok

#return localhost met stijl document
def csvStijl():
    df = pandas.read_csv("Pokemon.csv")
    return render_template("test_template.html", abc=[25, 12])

#return json file van csv
def csvJSON():
    df = pandas.read_csv("Pokemon.csv")    
    return df.to_json()


def azuredatabaseconnectie():
    server = 'yc2207hardloopserver.database.windows.net'
    database = 'yc2207bigdata'
    username = 'hardloop'
    password = 'abcd1234ABCD!@#$'
    driver= '{ODBC Driver 17 for SQL Server}'

    with odbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dbo.Table_1")
            row = cursor.fetchall()
            print(row)

def ShowGraph():
    mijndb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sport"
    )

    mijncursor = mijndb.cursor()
    baseSQL = "SELECT datum, Tijd FROM run WHERE GebruikerID = %s AND RouteID = %s"
    Specifics = (7, 123)
    mijncursor.execute(baseSQL, Specifics);
    recordset = mijncursor.fetchall()

    # for x in recordset:
    #     print("id nr:", x[0], " naam: ", x[1])

    df1 = pd.DataFrame(recordset, columns=["DatumTijd", "Seconden"])
    print(df1)

    fig = px.line(df1, x="DatumTijd", y="Seconden", title='Tijd in seconden voor route 123 van toby')
    fig.show()
    
    print("---------============== einde execute")
    return "see new tab"

    return "works"
