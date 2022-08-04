import plotly.graph_objects as go
import plotly.express as px 
import pandas as pd


def vanFelix1():


    # data
    df = pd.DataFrame({'x':['cars', 'fietsen', 'karts', 'motor'],
                        '2006':[1, 4, 9, 16],
                        '2007':[1, 4, 9, 16],
                        '2008':[6, 8, 4.5, 8]})
    df = df.set_index('x')

    # calculations
    # column sums for transposed dataframe
    sums= []
    for col in df.T:
        sums.append(df.T[col].sum())

    # change dataframe format from wide to long for input to plotly express
    df = df.reset_index()
    df = pd.melt(df, id_vars = ['x'], value_vars = df.columns[1:])

    fig = px.bar(df, x='x', y='value', color='variable')
    fig.data[-1].text = sums

    fig.update_traces(textposition='inside')
    fig.show()
    return "dit is een methode van Felix2"
