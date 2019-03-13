# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

seeds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
seed_wins = [21,5,4,1,0,1,1,1,0,0,0,0,0,0,0,0]

# initialize Dash environment
app = dash.Dash(__name__)

# set up an layout
app.layout = html.Div(children=[
    # H1 title on the page
    html.H1(children="NCAA Men's Basketball Tournament Championships by Seed"),

    # a div to put a short description
    html.Div(children='''
        This visualization shows the number of times each seed has won the NCAA Men's Basketball Tournament.
    '''),

    # append the visualization to the page
    dcc.Graph(
        id='Championships graph',
        figure={
            # configure the data
            'data': [
                {'x': seeds, 'y': seed_wins, 'type': 'bar', 'name': 'Championships'}
            ],
            'layout': {
                'title': "NCAA Men's Basketball Tournament Championships by Seed"
            }
        }
    )
])

if __name__ == '__main__':
    # start the Dash app
    app.run_server(debug=True)




