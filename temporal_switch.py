from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from data import *


temporal_switch_layout = dbc.Container(
    children=[
        html.H2(html.Strong("Temporal analysis - Switch"), className="content-header"),
        html.Hr(),
        html.P("Ik ben een appel."),
    ],
    className="content-global-style"
)