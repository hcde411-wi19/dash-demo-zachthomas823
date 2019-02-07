# -*- coding: utf-8 -*-
import colorlover as cl
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from datetime import datetime

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

# get sum of each breakdown
ds = df.sum()

# Group by month
dg = df.groupby(pd.Grouper(key='Date', freq='1M')).sum()
dg.index = dg.index.strftime('%Y-%m')
dg.index.name = 'Month'

# define fields
fields = [title for title in list(dg) if title != "Date"]

# define colors 
colors = cl.scales[str(len(fields))]['qual']['Paired']
field_colors = {}
for idx, field in enumerate(fields):
    field_colors[field] = colors[idx]
    
# current highlighting trends (default to be empty, which will show all trends)
highlighted_usage = set()

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
    html.H1(children='Trigger changes of one plot from another plot'),

    # set the description underneath the heading
    html.Div(children='''
        A demo to show how to make the plots connected.
    '''),

    # put charts in a div 
    html.Div(children=[

        # the first graph is a barchart
        dcc.Graph(
            id='trail-usage',
            figure={
                # configure the data
                'data': [{
                    # set x to be usage breakdown, and y to be the counts. We use bars to represent our data
                    'x': ds.index,
                    'y': ds.tolist(),
                    'type': 'bar',
                    'marker': {
                        'color': colors
                    }
                },
                ],
                # configure the layout of the visualization -- set the title to Total usage of the BGT North of NE 70th
                'layout': {
                    'title': 'Total usage of the BGT North of NE 70th'
                },
            },
            clickData={"points": []},
            config={'displayModeBar': False},
            style={
                'width': 500
            }
        ),

        # the second graph is a time series
        dcc.Graph(
            id='trend-series',
            config={'displayModeBar': False},
            clickData={"points": []}, style={
                'width': 800
            }
        ),
    ], style={
        'display': 'flex',
        'height': 500
    })

], style={
    'text-align': 'center'
})


# define interaction: when click on the bar chart, the highlighting of the time series will be changed
@app.callback(
    dash.dependencies.Output('trend-series', 'figure'),
    [dash.dependencies.Input('trail-usage', 'clickData')])
def update_graph(click_data):
    series = []

    for point in click_data["points"]:
        if point["x"] not in highlighted_usage:
            highlighted_usage.add(point["x"])
        elif point["x"] in highlighted_usage:
            highlighted_usage.remove(point["x"])

    for idx, field in enumerate(fields):
        if len(highlighted_usage) == 0 or field in highlighted_usage:
            series.append(
                go.Scatter(
                    x=dg.index,
                    y=dg[field],
                    mode='lines+markers',
                    name=field,
                    marker={
                        'color': field_colors[field]
                    }
                )
            )

    return {
        'data': series,
        'layout': {
            'title': 'Monthly usage of the BGT North of NE 70th over time'
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)