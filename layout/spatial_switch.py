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
	data_frame, color = None, 'black'
	if spatial_switch_type_input == "Overall":
		data_frame = overspeed
		color="black"
	elif spatial_switch_type_input == "Straight":
		data_frame = overspeed[overspeed["is_straight"] == True]
		color="red"
	elif spatial_switch_type_input == "Turning":
		data_frame = overspeed[overspeed["is_straight"] == False]
		color="blue"
	data_frame = data_frame[["switch_number", "latitude", "longitude", "speed", ]]
	data_frame = data_frame.groupby(["switch_number", "latitude", "longitude"]).count()
	data_frame.reset_index(inplace=True)
	overview_map_figure = dl.Map(
		children=[
			dl.TileLayer(),
			*[dl.CircleMarker(
				center=[row["latitude"], row["longitude"]],
				radius=row["speed"] / 5000,
				color=color) for _, row in data_frame.iterrows()],
		],
		center=[52.08, 4.30],
		zoom=13,
		style={
			"height": "40vh",
			"width": "100%"
		}
	)
	return [overview_map_figure, ]


@callback(
	[Output("spatial_switch_cdf", "figure"), ],
	[Input("spatial_switch_type_input", "value"), ]
)
def gen_spatial_switch_cdf(spatial_switch_type_input):
	data_frame = None
	if spatial_switch_type_input == "Overall":
		data_frame = overspeed
	elif spatial_switch_type_input == "Straight":
		data_frame = overspeed[overspeed["is_straight"] == True]
	elif spatial_switch_type_input == "Turning":
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
		html.H2("Spatial analysis "),
		html.H4([dbc.Badge("Switch", color="danger", pill=True)]),
		html.Hr(),
		dbc.Container(
			children=[
				# Type of overspeed:
				html.P(html.B("Overspeed type:"), style={"display": "inline-block"}),
				dcc.Dropdown(
					options=["Overall", "Straight", "Turning"],
					value="Overall",
					id="spatial_switch_type_input",
					style={"width": "10rem", "display": "inline-block", "margin-left": "1rem"}),
				# Number of Switch:
				html.P(html.B("#Switch:"), style={"display": "inline-block", "margin-left": "2rem"}),
				dcc.Dropdown(
					options=speed["switch_number"].unique(),
					value="W127",
					id="spatial_switch_input",
					style={"width": "10rem", "display": "inline-block", "margin-left": "1rem"},
				)
			],
			style={
				"display": "inline-block",
			}
		),
		# Left part:
		dbc.Container(spatial_switch_map, style={
			"width": "100%", "height": "42vh",}),
		html.Hr(),
		# Right part:
		dbc.Container(
			children=[
				# Cumulative density function
				spatial_switch_cdf,
			],
			style={
				"width": "30%",
				# "height": "85vh",
				"margin-left": "0%",
				# "margin-top": "-100vh",
				# "padding": "0.5vw",
				# "background-color": "rgb(255,10,220)",
				# "display": "inline-block",
			},
		)
	],
	style={
		"width": "90%",
		"height": "100vh",
		"margin-left": "10%",
		"margin-top": "-100vh",
		# "display": "inline-block",
	}
)
