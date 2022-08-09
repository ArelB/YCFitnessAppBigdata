import pyodbc as odbc
import plotly.express as px
import pandas as pd
import datetime

def printhome():
    return "hey"

def ShowGraph(persoon):

    #bepalen wat meest recente bestand is:
    server = 'yc2207hardloopserver.database.windows.net'
    database = 'yc2207backend'
    username = 'hardloop'
    password = 'abcd1234ABCD!@#$'
    driver= '{ODBC Driver 17 for SQL Server}'

    with odbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            # cursor.execute("SELECT R.DateAndTime, R.Duration FROM dbo.[User] U INNER JOIN Run R ON R.UserID = U.ID WHERE U.UserName = '"+persoon+"' AND RouteID = 9")
            # row = cursor.fetchall()
            sql_query = pd.read_sql_query("SELECT R.DateAndTime, R.Duration FROM dbo.[User] U INNER JOIN Run R ON R.UserID = U.ID WHERE U.UserName = '"+persoon+"' AND RouteID = 9", 
            conn, parse_dates={"DateAndTime": {"format": "%Y%M%d %H%M"}, "Duration": {"format": "%H%M"}})

            
            df = pd.DataFrame(sql_query, columns=["DateAndTime", "Duration"])

    df["Durationsec"] = 0

    for idx, x in enumerate(df["Duration"]):
        df["Durationsec"].iloc[idx] = (x.hour * 60 + x.minute) * 60 + x.second    
    
    print(df)
    df = df.sort_values(by="DateAndTime")
    fig = px.line(df, x="DateAndTime", y="Durationsec", title="Tijd route 9 van "+persoon, markers=True)
    fig.show()
    
    # print("---------============== einde execute")
    return "see new tab"