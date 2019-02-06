import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# initialize Dash app
app = dash.Dash(__name__)

# set the layout to have an input box and a div
app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])

# define callback to connect the input value with the content of the div
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

# start the app
if __name__ == '__main__':
    app.run_server()
    
    
    
