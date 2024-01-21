import dash
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
		legend=dict(x=0.9, y=0.99),
		margin=dict(l=0, r=0, t=25, b=10),
		xaxis_title=f"#Tramline",
	)
	return [tramline_histogram,]


@callback(
	[Output("spatial_tramline_speed_histogram", "figure")],
	[Input("spatial_tramline_input", "value"),
	 Input("spatial_tramline_type_input", "value")])
def gen_spatial_tramline_speed_histogram(spatial_tramline_input, spatial_tramline_type_input):
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
		data_frame, x="speed", y="is_straight", log_y=True, range_x=[15, 50])
	return [histogram_speed,]


tramline_type_input = dcc.Dropdown(
	options=["overall", "straight", "turning"], value="overall", id="spatial_tramline_type_input",
	style={
		"width": "20vw",
		"display": "inline-block",
		"margin-left": "1rem",
	})
histogram_tramline = dcc.Graph(
	id="spatial_tramline_histogram",
	style={"height": "30vh"})
tramline_input = dcc.Dropdown(options=speed["line"].unique(), value=1, id="spatial_tramline_input")
histogram_speed_tramline = dcc.Graph(
	id="spatial_tramline_speed_histogram",
	style={"height": "50vh"})

spatial_tramline_layout = html.Div(
	children=[
		html.H2("Spatial analysis"),
		html.H4([dbc.Badge("Tramline", color="danger", pill=True)]),
		html.Hr(),
		html.Div(
			children=[
				html.Label("HAHA:"),
				tramline_type_input,
			],
		),
		histogram_tramline,
		html.Hr(),
		tramline_input,
		histogram_speed_tramline,
	],
	className="content_container",
)