# import sys

import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import plotly
import plotly.graph_objects as go
import plotly.express as px

from sidebar import sidebar
from overview import overview_layout
from spatial_tramline import spatial_tramline_layout
from spatial_switch import spatial_switch_layout
from temporal_tramline import temporal_tramline_layout
from temporal_switch import temporal_switch_layout


# print(f"Python version: {sys.version}")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

content = dbc.Container(
    id="content",
    style={
        "left": "30rem",
        "margin": "auto",
        "text-align": "center"
    },
)

app.layout = dbc.Container(
    children=[
        dcc.Location(id="url"),
        sidebar,
        content
    ],
    className="container",

)

@app.callback(Output("content", "children"),
              Input("url", "pathname"))
def render_content(pathname):
    """
    The callback function that selects the content throught the sidebar.

    :param pathname: the url of the navlink points to.
    :return: the centent that the navlink points to.
    """
    if pathname == "/":
        return overview_layout
    elif pathname == "/spatial_tramline":
        return spatial_tramline_layout
    elif pathname == "/spatial_switch":
        return spatial_switch_layout
    elif pathname == "/temporal_tramline":
        return temporal_tramline_layout
    elif pathname == "/temporal_switch":
        return temporal_switch_layout


if __name__ == '__main__':
    app.run_server(debug=True, port=10010)

# TODO:
# 1. scalable layout
# 3. Interactive UX
# 2. CSS beautification


#TODO: 3 spatial-switch layout
#TODO: 4 temporal-tramline layout
#TODO: 5 temporal-switch layout