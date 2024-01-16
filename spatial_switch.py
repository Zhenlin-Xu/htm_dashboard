from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from data import *


spatial_switch_layout = dbc.Container(
    children=[
        html.H2(html.Strong("Spatial analysis - Switch"), className="content-header"),
        html.H4("Switch", className="content-header-2nd"),
        html.Hr(),
    ],
    className="content-global-style"
)