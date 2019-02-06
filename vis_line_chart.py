# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd

# initialize Dash app and initialize the static folder
app = dash.Dash(__name__, static_folder='static')
df = pd.read_json('static/bgt_bike_and_peds.json')

# Data clean up
for col in df.columns:
    if col == "Date":
        continue
    df[col] = df[col].replace(r'', np.nan, regex=True)
    df[col] = df[col].fillna(0)
    df[col] = pd.to_numeric(df[col])

# Group by month
dg = df.groupby(pd.Grouper(key='Date', freq='1M')).sum()
dg.index = dg.index.strftime('%Y-%m')
dg.index.name = 'Month'

fields = [title for title in list(dg) if title != "Date"]

# define lines - for each usage data, we create a line series through go.Scatter with mode 'lines+markers'
series = []
for title in fields:
    series.append(
        go.Scatter(
            x=dg.index,
            y=dg[title],
            mode='lines+markers',
            name=title
        )
    )


# set layout of the page
app.layout = html.Div(children=[

    # set the page heading
    html.H1(children='Line Chart'),

    # set the description underneath the heading
    html.Div(children='''
        A demo to show a line chart.
    '''),

    # append the visualization to the page
    dcc.Graph(
        id='example-graph',
        figure={
            # configure the data
            'data': series,
            'layout': {
                'title': 'Monthly usage of the BGT North of NE 70th over time',
            }
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)