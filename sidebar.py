from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "10rem",
    "padding": "1rem",
    "background-color": "#f8f9fa",
}

#TODO: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
sidebar = dbc.Nav(
    children=[
        dbc.NavLink("Overview", href="/", active="exact"),
        html.Hr(),
        # dbc.NavLink("Spatial analysis", href='/spatial', active="exact"),
        html.P("Spatial analysis"),
        dbc.NavLink("Switch", href='spatial/switch', active="exact"),
        dbc.NavLink("Tramline", href='spatial/tramline', active="exact"),
        html.Hr(),
        # dbc.NavLink("Temporal analysis", href='/temporal', active="exact"),
        html.P("Temporal analysis"),
        dbc.NavLink("Switch", href='temporal/switch', active="exact"),
        dbc.NavLink("Tramline", href='temporal/tramline', active="exact"),
    ],
    vertical=True,
    pills=True,
    style=SIDEBAR_STYLE,
)