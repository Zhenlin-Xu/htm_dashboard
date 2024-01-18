import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output


sidebar_layout = dbc.Nav(
	children=[
		html.P("Dashboard"),
		dbc.NavLink("Overview", href="/", active="exact"),
		html.Hr(),
		html.P("Spatial analysis"),
		dbc.NavLink("Switch", href='spatial_switch', active="exact"),
		dbc.NavLink("Tramline", href='spatial_tramline', active="exact"),
		html.Hr(),
		html.P("Temporal analysis"),
		dbc.NavLink("Switch", href='temporal_switch', active="exact"),
		dbc.NavLink("Tramline", href='temporal_tramline', active="exact"),
		html.Hr(),
	],
	vertical=True,
	pills=True,
	id="sidebar_container",
)