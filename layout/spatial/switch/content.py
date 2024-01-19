import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import html, dcc, Input, Output, callback
import plotly.express as px

from data_process.data import (
	speed, overspeed, straight_overspeed, turning_overspeed
)


@callback(
	[Output("spatial_switch_map", "children"), ],
	[Input("spatial_switch_type_input", "value"), ]
)
def gen_spatial_switch_map(spatial_switch_type_input):
	data_frame = None
	if spatial_switch_type_input == "overall":
		data_frame = overspeed
	elif spatial_switch_type_input == "straight":
		data_frame = overspeed[overspeed["is_straight"] == True]
	elif spatial_switch_type_input == "turning":
		data_frame = overspeed[overspeed["is_straight"] == False]

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
		style={"height": "83vh", "width": "24vw"}
	)
	return [overview_map_figure, ]


@callback(
	[Output("spatial_switch_cdf", "figure"), ],
	[Input("spatial_switch_type_input", "value"), ]
)
def gen_spatial_switch_cdf(spatial_switch_type_input):
	data_frame = None
	if spatial_switch_type_input == "overall":
		data_frame = overspeed
	elif spatial_switch_type_input == "straight":
		data_frame = overspeed[overspeed["is_straight"] == True]
	elif spatial_switch_type_input == "turning":
		data_frame = overspeed[overspeed["is_straight"] == False]
	# groupby
	data_frame = data_frame[["switch_number", "line"]].groupby("switch_number").count()
	data_frame.reset_index(inplace=True)

	cdf_figure = px.ecdf(
		data_frame=data_frame,
		x="line",
	)
	cdf_figure.update_layout(
		margin=dict(l=0, r=10, t=15, b=15),
		xaxis_title=f"#{spatial_switch_type_input} overspeeding records.",
		yaxis_title="",
		# title=f"Cumulative density function"
	)
	return [cdf_figure,]


spatial_switch_map = dbc.Container(id="spatial_switch_map", style={"display": "initial"})
spatial_switch_cdf = dcc.Graph(id="spatial_switch_cdf", style={"width": "24vw", "height": "35vh"})

spatial_switch_layout = html.Div(
	children=[
		html.H2("Spatial analysis"),
		html.H4("Switch"),
		html.Hr(),
		dbc.Container(
			children=[
				# dropdown button: type of overspeeding
				dcc.Dropdown(
					options=["overall", "straight", "turning"], value="overall", id="spatial_switch_type_input",
					style={"width": "5vw"}),
				# horizontal line
				# html.Hr(),
				# Map
				spatial_switch_map,
			],
			style={
				"width": "25vw",
				"height": "90vh",
				"background-color": "rgb(255,220,10)",
				"margin-left": "0.1vw",
				"padding": "0.5vw",
				# "display": "flex",
			},
		),
		dbc.Container(
			children=[
				# Cumulative density function
				spatial_switch_cdf,
			],
			style={
				"width": "17vw",
				"height": "90vh",
				"background-color": "rgb(255,20,210)",
				"margin-left": "25vw",
				"margin-top": "-90vh",
				"padding": "0.5vw",
				"display": "flex",
			},
		)
	],
	className="content_container",
)
