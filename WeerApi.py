from flask import render_template
import json
import requests
from pathlib import Path
from netCDF4 import Dataset
import datetime
import pyodbc as odbc

#api call van KNMI nieuwste data + data opslaan in NC bestand
def ApiCall():
    
    api_url = "https://api.dataplatform.knmi.nl/open-data"
    api_version = "v1"
    
    #api call parameters
    api_key = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjJlZTgxMGM1Yjc3NDRkMWFiODY5YzcxZTNlODg1MTk5IiwiaCI6Im11cm11cjEyOCJ9"
    dataset_name = "Actuele10mindataKNMIstations"
    dataset_version = "2"
    max_keys = "200"

    timestamp = datetime.datetime.utcnow().date().strftime("%Y%m%d")
    start_after_filename_prefix = f"KMDS__OPER_P___10M_OBS_L2_{timestamp}"

    #api call voor recente data
    reqresult = requests.get(
        f'{api_url}/datasets/{dataset_name}/versions/{dataset_version}/files',
        headers={"Authorization": api_key},
        params={"maxKeys": max_keys, "startAfterFilename": start_after_filename_prefix})

    #api call om meest recente data op te slaan
    list_files = reqresult.json()
    weer = list_files.get("files")

    filename = weer[-1].get("filename")
    endpoint = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files/{filename}/url"
    get_file_response = requests.get(endpoint, headers={"Authorization": api_key})

    download_url = get_file_response.json().get("temporaryDownloadUrl")
    dataset_file_response = requests.get(download_url)

    #NC bestand opslaan
    p = Path("ApiCallResults/"+filename)
    p.write_bytes(dataset_file_response.content)

    #apicall opslaan in database
    server = 'yc2207hardloopserver.database.windows.net'
    database = 'yc2207bigdata'
    username = 'hardloop'
    password = 'abcd1234ABCD!@#$'
    driver= '{ODBC Driver 17 for SQL Server}'


    weermetingdate = filename[26:30] + "-" + filename[30:32]+ "-" + filename[32:34] + " " + filename[34:36] + ":" + filename[36:38]
    print(weermetingdate)
    timestamp2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(timestamp2)
    query = "INSERT INTO [dbo].[KNMI_ApiCalls] ([Path],[ApiCallDatumTijd],[MeetDatumTijd])VALUES('ApiCallResults/"+filename+"','"+timestamp2+"', '"+weermetingdate+"')"
    print(query)
    with odbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

    return "[" + timestamp2 + "]: De meest recente weergegevens die u heeft opgevraagt zijn opgeslagen in de map ApiCallResults onder de naam: "+ filename

def homepagina():


    return render_template('apiweerhome.html')


def NCdata(loc):
    #bepalen wat meest recente bestand is:
    server = 'yc2207hardloopserver.database.windows.net'
    database = 'yc2207bigdata'
    username = 'hardloop'
    password = 'abcd1234ABCD!@#$'
    driver= '{ODBC Driver 17 for SQL Server}'

    with odbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM [dbo].[KNMI_ApiCalls]")
            row = cursor.fetchall()
    
    filename = str(row[-1][1])

    #open NC bestand
    rootgrp = Dataset(filename, "r", format="NETCDF4")

    #voor navigatie in NC bestand
    # print(rootgrp.__dict__)
    # for dim in rootgrp.dimensions.values():
    #     print(dim)
    # print(rootgrp.dimensions['time'])
    # print(rootgrp.variables.keys())
    print(rootgrp.variables['stationname'][:])
    # print(rootgrp.variables['rh'][:])
    # print(len(rootgrp.variables['stationname']))
    # print(len(rootgrp.variables['rh']))
    # print(int(rootgrp.variables["time"][0]))
    # print(VanafDatum)

    getal = 0
    loc = loc.replace(":", ' ')
    for idx, x in enumerate(rootgrp.variables['stationname']):
        if x == loc: 
            getal = idx
    print(getal)
    
    VanafDatum = datetime.datetime(1950,1,1,0,0,0) # year month day hour minute second
    MetingDatum = VanafDatum + datetime.timedelta(0, int(rootgrp.variables["time"][0]))

    locatieTijd = "Weer gegevens voor weermeetpunt: " + rootgrp.variables['stationname'][getal].lower() + " om " +  str(MetingDatum)
    Temperatuur = "De temperatuur is: " + str(rootgrp.variables["ta"][getal][0]) + " graden Celcius"
    Luchtvochtigheid = "De luchtvochtigheid is: " + str(rootgrp.variables["rh"][getal][0]) + " %"
    Wind = "De windsnelheid is: " + str(rootgrp.variables["ff"][getal][0]) +  "m/s" + " en de windvlaagsnelheid kan " + str(rootgrp.variables["gff"][getal][0]) + "m/s behalen"
    Neerslag = "Er is " + str(rootgrp.variables["R1H"][getal][0]) + " mm neerslag gevallen over " + str(rootgrp.variables["D1H"][getal][0]) + "minuten in het afgelopen uur"

    TempWaarschuwing = 'De temperatuur is prima'
    LuchtvochtigheidWaarschuwing = 'De luchtvochtigheid is prima'
    WindWaarschuwing = 'De windsnelheid is prima'
    NeerslagWaarschuwing = 'Er is geen neerslag in het afgelopen uur'
    GladSneeuwWaarschuwing = 'Er is geen sneeuw of gladheid'

    if rootgrp.variables["ta"][getal] < 5 or rootgrp.variables["ta"][getal] > 25: TempWaarschuwing = "Pas op! De temperatuur is buiten 5 tot 25 graden celsius"
    if rootgrp.variables["rh"][getal] > 85: LuchtvochtigheidWaarschuwing = "Pas op! De luchtvochtigheid is hoger dan 85%, je kan minder makkelijk afkoelen, zeker bij hoge temperaturen"
    if rootgrp.variables["ff"][getal] > 75 or rootgrp.variables["gff"][getal] > 75: WindWaarschuwing = "Pas op! De wind kan meer dan 75 km/u halen"
    if rootgrp.variables["R1H"][getal] > 0: NeerslagWaarschuwing = "Pas op! het heeft in het afgelopen uur geregend en is mogelijk nog bezig"
    if rootgrp.variables["R1H"][getal] > 0 and rootgrp.variables["ta"][getal] < 0: GladSneeuwWaarschuwing = "Pas op! Het heeft in het afgelopen uur geregend en de temperatuur is onder 0 C. Er kan sneeuw liggen en het kan glad zijn"

    rootgrp.close()

    return render_template("Weer_template.html", returnlist = [str(locatieTijd), str(Temperatuur), str(Luchtvochtigheid), str(Wind), str(Neerslag), str(TempWaarschuwing), str(LuchtvochtigheidWaarschuwing), str(WindWaarschuwing), str(NeerslagWaarschuwing), str(GladSneeuwWaarschuwing)])