import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import plotly.graph_objs as go

import urllib.parse, urllib.request, urllib.error, json
appid = "76997c3de4614862d678953c9cef0647"
baseurl = "http://api.openweathermap.org/data/2.5/forecast"

def getWeather(city):
    try:
        params = {
            "q": city,
            "appid": appid,
            "mode": 'json',
            "units": 'imperial'  # or "metric"
        }
        paramstr = urllib.parse.urlencode(params)
        weatherrequest = baseurl + '?' + paramstr

        response = urllib.request.urlopen(weatherrequest)
        weatherjsonstr = response.read()
        weatherdata = json.loads(weatherjsonstr)
        return weatherdata
    except:
        return None

def getTemperatureData(city):
    data = getWeather(city)
    if data:
        wtime = []
        wtemp = []
        for forecast in data['list']:
            time = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
            temp = forecast['main']['temp']
            wtime.append(time)
            wtemp.append(temp)
        return wtime, wtemp
    else:
        return None

# initialize Dash app
app = dash.Dash(__name__)

# set up an layout
app.layout = html.Div(children=[
    # H1 title on the page
    html.H1(children='Input box + Line Chart'),

    # a div to put a short description
    html.Label(children='Enter a city name:'),

    dcc.Input(id='city', value='Seattle', type='text'),

    # append the visualization to the page
    dcc.Graph(
        id='linechart'
    )
])
@app.callback(
    Output(component_id='linechart', component_property='figure'),
    [Input(component_id='city', component_property='value')]
)
def get_data(city):
    data = getTemperatureData(city)
    if data:
        wtime, wtemp = data
        return {
            # configure the data
            'data': [
                # Step 3: set x to be time, and y to be the temperature.
                # We use line chart to represent our data.
                go.Scatter(
                    x=wtime,
                    y=wtemp,
                    mode='lines+markers'
                )
                # To use barchart, simply replace the above four lines with
                # {'x': wtime, 'y': wtemp, 'type': 'bar'},
            ],
            # configure the layout of the visualization
            'layout': {
                # Step 4: Set the title to be '5 day temperature forecast of "' + city + '"'
                'title': '5 day temperature forecast of "' + city + '"'
            }
        }
    else:
        return {}

# start the app
if __name__ == '__main__':
    app.run_server()

