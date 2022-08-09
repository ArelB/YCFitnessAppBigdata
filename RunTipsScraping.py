import requests
import random
from bs4 import BeautifulSoup
from flask import render_template

def GetTip():

    pagina = requests.get('https://www.theguardian.com/lifeandstyle/2017/aug/14/running-beginners-10-tips-parkrun-exercise-run-jog-5k')

    #print(pagina.content)

    heeldehtml = BeautifulSoup(pagina.content, 'html.parser')

    TitleTips = heeldehtml.find_all('h2')
    del TitleTips[-2:]
    for x in TitleTips:
        print(type(x.get_text()))
    
    BodyTips = heeldehtml.find_all("p")
    del BodyTips[:5]
    del BodyTips[-1:]
    for x in BodyTips:
        print(x.get_text())
    # #nu is het al veel duidelijker maar nog steeds een hoop dingen, zie hieronder
    nummer = random.randint(0,9)

    textnr = ""

    if nummer == 0:
        textnr = [0,1]
    elif nummer == 1:
        textnr = [2,3,4]
    elif nummer == 2:
        textnr = [5,6,7]
    elif nummer == 3:
        textnr = [8,9,10]
    elif nummer == 4:
        textnr = [11,12,13]
    elif nummer == 5:
        textnur = [14,15,16]
    elif nummer == 6:
        textnr = [17,18]
    elif nummer == 7:
        textnr = [19,20,21]
    elif nummer == 8:
        textnr = [22,23]
    elif nummer == 9:
        textnr = [24,25]

    print("=======================================================")
    bodytip = ""

    print(TitleTips[nummer].text)
    for x in textnr:
        print(BodyTips[x])
        bodytip = bodytip + str(BodyTips[x].text) + " "

    # #je kan het ook iets meer leesbaar maken met prettify
    # #print(tabel.prettify())

    # #op deze manier kan je loopen over de verschillende rijen en heel specifiek een waarde krijgen
    # allerijen = tabel.find_all('tr')

    # x = 0 
    # for rij in allerijen:
    #     x = x + 1
    #     print(rij)
    #     cel = rij.find(class_="sc-131di3y-0")
    #     print(cel.find('span').text)
    #     if x > 1:
    #         break

    return render_template("runtip_template.html", runtip = [TitleTips[nummer].text, bodytip])