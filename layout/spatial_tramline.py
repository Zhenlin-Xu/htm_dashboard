import numpy as np
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import plotly.express as px

from data_process.data import (
	speed, overspeed, straight_overspeed, turning_overspeed
)


@callback(
	[Output("spatial_tramline_histogram", "figure")],
	[Input("spatial_tramline_type_input", "value")])
def gen_spatial_tramline_histogram(spatial_tramline_type_input):
	# specify the type of overspeed
	data_frame = None
	if spatial_tramline_type_input == "overall":
		data_frame = overspeed[["line", "speed", "is_straight"]]
	elif spatial_tramline_type_input == "straight":
		data_frame = overspeed[["line", "speed", "is_straight"]]
		data_frame = data_frame[data_frame["is_straight"] == True]
	elif spatial_tramline_type_input == "turning":
		data_frame = overspeed[["line", "speed", "is_straight"]]
		data_frame = data_frame[data_frame["is_straight"] == False]

	tramline_grpby = data_frame.groupby(["is_straight", "line"]).count()
	tramline_grpby.reset_index(inplace=True)
	tramline_grpby.set_index("line", inplace=True)

	tramline_histogram = px.bar(
		data_frame=tramline_grpby,
		x=[str(i) for i in tramline_grpby.index],
		y="speed",
		color="is_straight",
		range_y=[0, 450_000],
		title=f"The {spatial_tramline_type_input} overspeed distribution of all tram line.",
	)
	tramline_histogram.update_layout(
		legend=dict(x=0.9, y=0.99, title="Type"),
		# margin=dict(l=0, r=0, t=25, b=10),
		xaxis_title=f"#Tramline",
		yaxis_title=f"#Overspeed records",
	)
	return [tramline_histogram, ]


@callback(
	[Output("spatial_tramline_speed_histogram", "figure")],
	[Input("spatial_tramline_input", "value"),
	 Input("spatial_tramline_type_input", "value"),
	 Input("spatial_tramline_logy_button", "value"), ])
def gen_spatial_tramline_speed_histogram(
		spatial_tramline_input,
		spatial_tramline_type_input,
		spatial_tramline_logy_button
):
	data_frame = None
	if spatial_tramline_type_input == "overall":
		data_frame = overspeed[overspeed["line"] == spatial_tramline_input]
		data_frame = data_frame[["speed", "is_straight"]]
	elif spatial_tramline_type_input == "straight":
		data_frame = overspeed[(overspeed["is_straight"] == True) & (overspeed["line"] == spatial_tramline_input)]
		data_frame = data_frame[["speed", "is_straight"]]
	elif spatial_tramline_type_input == "turning":
		data_frame = overspeed[(overspeed["is_straight"] == False) & (overspeed["line"] == spatial_tramline_input)]
		data_frame = data_frame[["speed", "is_straight"]]

	data_frame = data_frame.groupby("speed").count()
	data_frame.reset_index(inplace=True)
	histogram_speed = px.bar(
		data_frame, x="speed", y="is_straight",
		log_y=True if spatial_tramline_logy_button == "log" else False,
		range_x=[15, 50],
		title=f"The number of overspeed records in tramline {spatial_tramline_input}."
	)
	histogram_speed.update_layout(
		xaxis_title="Speed",
		yaxis_title="#Overspeed records",
	)
	return [histogram_speed, ]

@callback(
	[Output("spatial_tramline_response", "children")],
	[Input("spatial_tramline_type_input", "value")]
)
def spatial_tramline_response(spatial_tramline_type_input):
	return [
		f"""
		Hello, you have selected {spatial_tramline_type_input} as the type of overspeed :)
		""",
	]


@callback(
	[Output("spatial_tramline_response2", "children"), ],
	[Input("spatial_tramline_input", "value"),
	 Input("spatial_tramline_logy_button", "children"), ]
)
def spatial_tramline_response2(
		spatial_tramline_input,
		spatial_tramline_logy_button
):
	logy_button = "" if spatial_tramline_logy_button == "log" else "not"
	return [
		f"""Hello, you have selected tramline {spatial_tramline_input} 
		and the histogram's y-axis is {logy_button} in log-scale :)"""
	]


tramline_type_input = dcc.Dropdown(
	options=["overall", "straight", "turning"], value="overall", id="spatial_tramline_type_input",
	style={
		"width": "8rem",
		"display": "inline-block",
		"margin-left": "1rem",
	}
)

histogram_tramline = dcc.Graph(
	id="spatial_tramline_histogram",
	style={"height": "35vh"})

tramline_input = dcc.Dropdown(
	options=np.sort(speed["line"].unique()),
	value=1,
	id="spatial_tramline_input",
	style={
		"width": "8rem",
		"display": "inline-block",
		"margin-left": "1rem",
	}
)
# COMPONENT: RadioItems to select the scale of the y-axis.
logY_button = dbc.RadioItems(
	options=["linear", "log"],
	value="Linear",
	id="spatial_tramline_logy_button",
	inline=True,
	style={
		"display": "inline-block",
		"margin-left": "1rem",
	}
)

histogram_speed_tramline = dcc.Graph(
	id="spatial_tramline_speed_histogram",
	style={"height": "40vh"})

spatial_tramline_layout = html.Div(
	children=[
		# Header:
		html.H2("Spatial analysis"),
		html.H4([dbc.Badge("Tramline", color="danger", pill=True)]),
		html.Hr(),
		# Upper options：
		html.Div(
			children=[
				html.P(html.B("Overspeed type:"), style={"display": "inline-block", "margin-left": "1rem"}),
				tramline_type_input,
			],
		),
		dbc.Badge(
			id="spatial_tramline_response",
			color="info",
			pill=True,
			style={
				"display": "inline-block",
				"margin-left": "2rem",
				"font-size": "medium",
			},
		),
		# Upper plot:
		histogram_tramline,
		html.Hr(),
		# Lower option:
		dbc.Container(
			children=[
				html.P(html.B("Y axis:"), style={"display": "inline-block", "margin-left": "1rem"}),
				logY_button,
				html.P(html.B("#Tramline:"), style={"display": "inline-block", "margin-left": "1rem"}),
				tramline_input]
		),
		dbc.Badge(
			id="spatial_tramline_response2",
			color="info",
			pill=True,
			style={
				"display": "inline-block",
				"margin-left": "2rem",
				"font-size": "medium"
			},
		),
		# Lower plot:
		histogram_speed_tramline,
	],
	style={
		"width": "90%",
		"height": "100vh",
		"margin-left": "10%",
		"margin-top": "-100vh",
		# "display": "inline-block",
	}
)
