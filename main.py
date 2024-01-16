# import sys

import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import plotly
import plotly.graph_objects as go
import plotly.express as px

from sidebar import sidebar
from overview import overview
from spatial_tramline import spatial_tramline_layout

# print(f"Python version: {sys.version}")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    children=[
        # html.H1("HTM Dashboard"),
        # html.Hr(),
        sidebar,
        spatial_tramline_layout,
        # overview,
    ],
)

app.run_server(debug=True, port=10010)

# TODO:
# 1. scalable layout
# 3. Interactive UX
# 2. CSS beautification


#TODO: 3 spatial-switch layout
#TODO: 4 temporal-tramline layout
#TODO: 5 temporal-switch layout