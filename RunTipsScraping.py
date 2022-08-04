import requests
from bs4 import BeautifulSoup

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
    print(TitleTips)

    print(BodyTips)

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

    return "hoi"