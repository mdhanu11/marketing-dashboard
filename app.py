import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import base64
import io

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Marketing Analytics Dashboard'),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-graph')
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return html.Div([
                'The file format is not supported. Please upload a CSV file.'
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing the file.'
        ])

    return html.Div([
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    go.Bar(
                        x=df['Day'],
                        y=df['Cost'],
                        name='Cost',
                        marker=dict(color='blue'),
                        yaxis='y1'
                    ),
                    go.Scatter(
                        x=df['Day'],
                        y=df['Clicks'],
                        mode='lines+markers',
                        name='Clicks',
                        line=dict(color='magenta'),
                        yaxis='y2'
                    ),
                    go.Scatter(
                        x=df['Day'],
                        y=df['Impr.'],
                        mode='lines+markers',
                        name='Impressions',
                        line=dict(color='green'),
                        yaxis='y3'
                    )
                ],
                'layout': go.Layout(
                    title='Cost, Clicks, and Impressions Over Days',
                    xaxis={'title': 'Day'},
                    yaxis=dict(
                        title='Cost',
                        titlefont=dict(color='blue'),
                        tickfont=dict(color='blue')
                    ),
                    yaxis2=dict(
                        title='Clicks',
                        titlefont=dict(color='magenta'),
                        tickfont=dict(color='magenta'),
                        overlaying='y',
                        side='right',
                        position=0.85
                    ),
                    yaxis3=dict(
                        title='Impressions',
                        titlefont=dict(color='green'),
                        tickfont=dict(color='green'),
                        overlaying='y',
                        side='right',
                        position=0.95
                    ),
                    legend={'x': 0, 'y': 1},
                    margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                    hovermode='closest'
                )
            }
        )
    ])

@app.callback(Output('output-graph', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        return parse_contents(contents, filename)
    return html.Div([
        'Please upload a CSV file.'
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
