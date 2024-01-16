from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from data import *


temporal_tramline_layout = dbc.Container(
    children=[
        html.H2(html.Strong("Temporal analysis - Tramline"), className="content-header"),
        html.Hr(),
    ],
    className="content-global-style"
)