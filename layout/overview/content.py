import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import dash_leaflet as dl

from data_process.data import *

round_rectangles = html.Div(
	children=[
		html.Div(
			[
				html.P("Overall overspeeding"),
				html.P(f"{len(overspeed)}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
		html.Div(
			[
				html.P("Straight overspeeding"),
				html.P(f"{len(straight_overspeed)}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
		html.Div(
			[
				html.P("Turning overspeeding"),
				html.P(f"{len(turning_overspeed)}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
		html.Div(
			[
				html.P("Percentage of overspeeding"),
				html.P(f"{len(overspeed) / len(speed):.2f}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
	],
	className ="round_rectangles"
)

overview_map_figure = dl.Map(
    children=[
        dl.TileLayer(),
        *[
            dl.CircleMarker(
                center=[52.08, 4.30],
                radius=100,
                color="red",
            )
        ]
    ],
    center=[52.08, 4.30],
    zoom=13,
    style={"height": "70vh", "width": "22vw", "margin-left": "-1rem", "background-color": "rgb(255, 255, 255)"}
)
overview_map = dbc.Container(
    children=overview_map_figure,
    style={"margin-top": "1rem"},
)

overview_layout = html.Div(
	children=[
		html.H2("Overspeeding dashboard"),
		html.H4("Overview"),
		html.Hr(),
		round_rectangles,
		overview_map,
	],
	className="content_container",
)
