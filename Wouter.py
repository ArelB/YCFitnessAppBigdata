import pandas

def csvFunctie():
    df = pandas.read_csv("pokemon.csv")    
    #flask.render_template("test_template.html")
    return str(df.columns)

def printPokemon(pok):
    df = pandas.read_csv("pokemon.csv") 
    return pok

# def hello(name=None):
#     return render_template('hello.html', name=name)