import pandas

def csvFunctie():
    df = pandas.read_csv("Pokemon.csv")    
    #flask.render_template("test_template.html")
    return str(df.columns)

def printPokemon(pok):
    df = pandas.read_csv("Pokemon.csv") 
    return pok

# def hello(name=None):
#     return render_template('hello.html', name=name)