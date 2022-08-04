import mysql.connector
import plotly.express as px
import pandas as pd

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