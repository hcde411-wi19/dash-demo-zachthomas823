# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly import tools
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
# We define this max_y variable to save the maximum value of possible counts
max_y = 0

# This is how you make a plot that contains multiple subplots.
# In this case, the number of rows are the number of fields,
# and the number of cols is one.
# The x axes are set to be shared so that all plots use the same one
fig = tools.make_subplots(rows=len(fields), cols=1, shared_xaxes=True)

for idx, title in enumerate(fields):
    trace = go.Scatter(
        x=dg.index,
        y=dg[title],
        mode='lines+markers',
        name=title
    )

    # Unlike the line chart example, we add a line (a trace) to the "fig" directly
    fig.append_trace(trace, idx + 1, 1)

    # Update max_y by comparing max_y with the max of the counts of this line
    max_y = max(max_y, dg[title].max())

# This for loop sets all the plots to have the same range of y axes.
for idx in range(len(fields)):
    fig['layout']["yaxis%d" % (idx + 1)].update(range=[0, max_y + 500])

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Small Multiples'),

    html.Div(children='''
        A example of small multiples for monthly usage of the BGT North of NE 70th over time.
    '''),

    dcc.Graph(
        id='example-graph',
        # Instead of having data and layout, now we set the figure through the "fig" we've created above
        figure=fig
    ),

])
if __name__ == '__main__':
    app.run_server(debug=True)