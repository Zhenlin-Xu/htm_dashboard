import dash
from dash import html
from dash import dcc

app = dash.Dash(name=__name__)

app.layout = html.Div([
    html.H1("HTM Dashboard")
])


if __name__ == '__main__':
    app.run_server(debug=True)
