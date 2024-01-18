import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output


spatial_switch_layout = html.Div(
	children=[
		html.H2("Spatial analysis"),
		html.H4("Switch"),
		html.Hr(),
	],
	className="content_container",
)