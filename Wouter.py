import pandas
from flask import render_template
import json
import requests
from pathlib import Path
from netCDF4 import Dataset
import datetime

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

filename = 'KMDS__OPER_P___10M_OBS_L2_202208040130.nc'

#api call van KNMI nieuwste data + data opslaan in NC bestand
def ApiCall():
    api_url = "https://api.dataplatform.knmi.nl/open-data"
    api_version = "v1"
    
    #api call parameters
    api_key = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjJlZTgxMGM1Yjc3NDRkMWFiODY5YzcxZTNlODg1MTk5IiwiaCI6Im11cm11cjEyOCJ9"
    dataset_name = "Actuele10mindataKNMIstations"
    dataset_version = "2"
    max_keys = "10"

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
    global filename

    filename = weer[-1].get("filename")
    endpoint = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files/{filename}/url"
    get_file_response = requests.get(endpoint, headers={"Authorization": api_key})

    download_url = get_file_response.json().get("temporaryDownloadUrl")
    dataset_file_response = requests.get(download_url)

    #NC bestand opslaan
    p = Path(filename)
    p.write_bytes(dataset_file_response.content)

    return filename


def NCdata():
    #open NC bestand
    rootgrp = Dataset(filename, "r", format="NETCDF4")

    #voor navigatie in NC bestand
    # print(rootgrp.__dict__)
    # for dim in rootgrp.dimensions.values():
    #     print(dim)
    # print(rootgrp.dimensions['time'])
    # print(rootgrp.variables.keys())
    # print(rootgrp.variables['stationname'].shape)
    # print(rootgrp.variables['rh'][:])
    # print(len(rootgrp.variables['stationname']))
    # print(len(rootgrp.variables['rh']))
    # print(int(rootgrp.variables["time"][0]))
    # print(VanafDatum)

    VanafDatum = datetime.datetime(1950,1,1,0,0,0) # year month day hour minute second
    MetingDatum = VanafDatum + datetime.timedelta(0, int(rootgrp.variables["time"][0]))

    locatieTijd = "Weer gegevens voor weermeetpunt: " + rootgrp.variables['stationname'][14].lower() + " om " +  str(MetingDatum)
    Temperatuur = "De temperatuur is: " + str(rootgrp.variables["ta"][14][0]) + " graden Celcius"
    Luchtvochtigheid = "De luchtvochtigheid is: " + str(rootgrp.variables["rh"][14][0]) + " %"
    Wind = "De windsnelheid is: " + str(rootgrp.variables["ff"][14][0]) +  "m/s" + " en de windvlaagsnelheid kan " + str(rootgrp.variables["gff"][14][0]) + "m/s behalen"
    Neerslag = "Er is " + str(rootgrp.variables["R1H"][14][0]) + " mm neerslag gevallen over " + str(rootgrp.variables["D1H"][14][0]) + "minuten in het afgelopen uur"

    TempWaarschuwing = 'De temperatuur is prima'
    LuchtvochtigheidWaarschuwing = 'De luchtvochtigheid is prima'
    WindWaarschuwing = 'De windsnelheid is prima'
    NeerslagWaarschuwing = 'Er is geen neerslag in het afgelopen uur'
    GladSneeuwWaarschuwing = 'Er is geen sneeuw of gladheid'

    if rootgrp.variables["ta"][14] < 5 or rootgrp.variables["ta"][14] > 25: TempWaarschuwing = "Pas op! De temperatuur is buiten 5 tot 25 graden celsius"
    if rootgrp.variables["rh"][14] > 85: LuchtvochtigheidWaarschuwing = "Pas op! De luchtvochtigheid is hoger dan 85%, je kan minder makkelijk afkoelen, zeker bij hoge temperaturen"
    if rootgrp.variables["ff"][14] > 75 or rootgrp.variables["gff"][14] > 75: WindWaarschuwing = "Pas op! De wind kan meer dan 75 km/u halen"
    if rootgrp.variables["R1H"][14] > 0: NeerslagWaarschuwing = "Pas op! het heeft in het afgelopen uur geregend en is mogelijk nog bezig"
    if rootgrp.variables["R1H"][14] > 0 and rootgrp.variables["ta"][14] < 0: GladSneeuwWaarschuwing = "Pas op! Het heeft in het afgelopen uur geregend en de temperatuur is onder 0 C. Er kan sneeuw liggen en het kan glad zijn"

    rootgrp.close()

    return render_template("Weer_template.html", returnlist = [str(locatieTijd), str(Temperatuur), str(Luchtvochtigheid), str(Wind), str(Neerslag), str(TempWaarschuwing), str(LuchtvochtigheidWaarschuwing), str(WindWaarschuwing), str(NeerslagWaarschuwing), str(GladSneeuwWaarschuwing)])

    