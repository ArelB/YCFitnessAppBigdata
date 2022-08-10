import pyodbc as odbc
import plotly.express as px
import pandas as pd
import datetime

def ShowGraph(persoon, route):

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
            Users = pd.read_sql_query("SELECT ID, UserName FROM dbo.[User]", conn)
            Routes = pd.read_sql_query("SELECT ID, Name FROM dbo.[Route]", conn)

            wherepersoon = "WHERE U.UserName = '"+persoon
            whereroute = "' AND RouteID = "+route

            if persoon in Users["UserName"].unique():
                wherepersoon = "WHERE U.UserName = '"+persoon
            elif int(persoon) in Users["ID"].unique():
                wherepersoon = "WHERE U.ID = '"+persoon
            else: return "De waarde die u heeft opgegeven voor gebruiker komt niet overeen met de naam of id van een gebruiker"

            if str(route) in Routes["Name"].unique():
                whereroute = "' AND RouteID = '"+ str(Routes.loc[Routes["Name"] == route, "ID"].iloc[0])
            else:
                try:
                    if int(route) in Routes["ID"].unique():
                        whereroute = "' AND RouteID = '"+route
                    else: return "De waarde die u heeft opgegeven voor route komt niet overeen met de naam of id van een route"
                except: return "De waarde die u heeft opgegeven voor route komt niet overeen met de naam of id van een route"

            wherestatement = wherepersoon + whereroute
            try:
                sql_query = pd.read_sql_query("SELECT R.DateAndTime, R.Duration FROM dbo.[User] U INNER JOIN Run R ON R.UserID = U.ID "+wherestatement+"'", 
                conn, parse_dates={"DateAndTime": {"format": "%Y%M%d %H%M"}, "Duration": {"format": "%H%M"}})

                df = pd.DataFrame(sql_query, columns=["DateAndTime", "Duration"])
            except:
                return "de combinatie van deze gebruiker en deze route heeft geen runs"
            
    df["Durationsec"] = 0

    print(Users)
    print(Routes)

    for idx, x in enumerate(df["Duration"]):
        df["Durationsec"].iloc[idx] = (x.hour * 60 + x.minute) * 60 + x.second    
    
    print(df)
    df = df.sort_values(by="DateAndTime")
    fig = px.line(df, x="DateAndTime", y="Durationsec", title="Tijd route "+route+" van "+persoon, markers=True)
    fig.show()
    
    # print("---------============== einde execute")
    return "see new tab"