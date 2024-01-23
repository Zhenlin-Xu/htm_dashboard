import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import html, dcc, Input, Output, callback
import plotly.express as px

from data_process.data import (
	speed, overspeed, straight_overspeed, turning_overspeed
)


@callback(
	[Output("spatial_switch_map_str", "children"),
	 Output("spatial_switch_map_trn", "children"),],
	[Input("spatial_switch_useless", "value"), ]
)
def gen_spatial_switch_map_str(spatial_switch_useless):
	data_frame = straight_overspeed
	data_frame = data_frame[["switch_number", "latitude", "longitude", "speed", ]]
	data_frame = data_frame.groupby(["switch_number", "latitude", "longitude"]).count()
	data_frame.reset_index(inplace=True)
	map_str = dl.Map(
		children=[
			dl.TileLayer(),
			*[dl.CircleMarker(
				id="str_"+str(row["switch_number"]),
				children=[
					dl.Tooltip(html.P(f"""
							#Switch   : {row["switch_number"]}\n
							Coordinate: ({row["latitude"]}, {row["longitude"]})\n
							#Records  : {row["speed"]}
							""",
							style={'white-space': 'pre-line'}
							))
				],
				center=[row["latitude"], row["longitude"]],
				radius=row["speed"] / 2000,
				color="red") for _, row in data_frame.sort_values("switch_number", ascending=False).iterrows()],
		],
		center=[52.08, 4.30],
		zoom=12.5,
		style={
			"height": "38vh",
			"width": "60%",
		}
	)
	data_frame = turning_overspeed
	data_frame = data_frame[["switch_number", "latitude", "longitude", "speed", ]]
	data_frame = data_frame.groupby(["switch_number", "latitude", "longitude"]).count()
	data_frame.reset_index(inplace=True)
	map_trn = dl.Map(
		children=[
			dl.TileLayer(),
			*[dl.CircleMarker(
				id="trn_"+str(row["switch_number"]),
				children=[
					dl.Tooltip(html.P(f"""
							#Switch   : {row["switch_number"]}\n
							Coordinate: ({row["latitude"]}, {row["longitude"]})\n
							#Records  : {row["speed"]}
							""",
							style={'white-space': 'pre-line'}
							))
				],
				center=[row["latitude"], row["longitude"]],
				radius=row["speed"] / 2000,
				color="blue") for _, row in data_frame.sort_values("switch_number", ascending=False).iterrows()],
		],
		center=[52.08, 4.30],
		zoom=12.5,
		style={
			"height": "38vh",
			"width": "60%",
		}
	)
	return [map_str, map_trn]

@callback(
	Output("spatial_switch_response1", "children"),
	[Input("str_"+str(switch), 'n_clicks') for switch in straight_overspeed["switch_number"].unique()]
)
def gen_str_response(*n_clicks_list):
	clicked_marker_id = dash.callback_context.triggered_id

	if clicked_marker_id is None:
		return "Select a marker by clicking on it."

	return f"Straight overspeed: switch {clicked_marker_id[4:]} has been clicked."


@callback(
	Output("spatial_switch_response2", "children"),
	[Input("trn_"+str(switch), 'n_clicks') for switch in turning_overspeed["switch_number"].unique()]
)
def gen_str_response(*n_clicks_list):
	clicked_marker_id = dash.callback_context.triggered_id

	if clicked_marker_id is None:
		return "Select a marker by clicking on it."

	return f"Turning overspeed: switch {clicked_marker_id[4:]} has been clicked."


@callback(
	[Output("spatial_switch_pdf_str", "figure"),],
	 [Input("str_"+switch, 'n_clicks') for switch in straight_overspeed["switch_number"].unique()]
)
def gen_str_cdf(*n_clicks_list):
	data_frame = straight_overspeed
	clicked_marker_id = dash.callback_context.triggered_id
	# groupby
	if clicked_marker_id is not None:
		data_frame = data_frame[data_frame["switch_number"] == clicked_marker_id[4:]]

	data_frame["#day_in_year"] = data_frame["#week"] * 7 + data_frame["#day"]
	data_frame = data_frame[["#day_in_year", "line"]].groupby("#day_in_year").count()
	data_frame.reset_index(inplace=True)

	pdf_figure = px.histogram(
		data_frame,
		x="#day_in_year",
		y="line",
		nbins=55,
	)
	pdf_figure.update_layout(
		margin=dict(l=0, r=10, t=15, b=15),
		xaxis=dict(tickmode="linear", range=[1, 365], dtick=50),
		xaxis_title=f"Time (in 2023)",
		yaxis_title="#Overspeed records",
	)
	return [pdf_figure]


@callback(
	[Output("spatial_switch_pdf_trn", "figure"),],
	 [Input("trn_"+switch, 'n_clicks') for switch in turning_overspeed["switch_number"].unique()]
)
def gen_trn_cdf(*n_clicks_list):
	data_frame = turning_overspeed
	clicked_marker_id = dash.callback_context.triggered_id
	# groupby
	if clicked_marker_id is not None:
		data_frame = data_frame[data_frame["switch_number"] == clicked_marker_id[4:]]

	data_frame["#day_in_year"] = data_frame["#week"] * 7 + data_frame["#day"]
	data_frame = data_frame[["#day_in_year", "line"]].groupby("#day_in_year").count()
	data_frame.reset_index(inplace=True)

	pdf_figure = px.histogram(
		data_frame,
		x="#day_in_year",
		y="line",
		nbins=55,
	)
	pdf_figure.update_layout(
		margin=dict(l=0, r=10, t=15, b=15),
		xaxis=dict(tickmode="linear", range=[1, 365], dtick=50),
		xaxis_title=f"Time (in 2023)",
		yaxis_title="#Overspeed records",
	)
	return [pdf_figure]

spatial_switch_map_str = dbc.Container(
	id="spatial_switch_map_str",
	style={
		"height": "38vh",
		"display": "inline-block",
	}
)
spatial_switch_map_trn = dbc.Container(
	id="spatial_switch_map_trn",
	style={
		"height": "38vh",
		"display": "inline-block",
	}
)
spatial_switch_pdf_str = dcc.Graph(
	id="spatial_switch_pdf_str",
	style={
		"height": "36vh",
		"width": "38%",
		"margin-left": "60%",
		"margin-top": "-100vh",
		"display": "inline-block",
	},
)
spatial_switch_pdf_trn = dcc.Graph(
	id="spatial_switch_pdf_trn",
	style={
		"height": "36vh",
		"width": "38%",
		"margin-left": "60%",
		"margin-top": "-100vh",
		"display": "inline-block",
	},
)

spatial_switch_layout = dbc.Container(
	children=[
		# Header:
		dbc.Container(
			[
				html.H2("Spatial analysis"),
				html.H4([dbc.Badge("Switch", color="danger", pill=True)]),
			],
			style={"padding": "0.3rem"}
		),
		html.Hr(id="spatial_switch_useless"),
		# Left part:
		spatial_switch_map_str, spatial_switch_pdf_str,
		dbc.Badge(id="spatial_switch_response1", color="danger", pill=True, style={"margin-left": "1rem"}),
		html.Hr(),
		spatial_switch_map_trn, spatial_switch_pdf_trn,
		dbc.Badge(id="spatial_switch_response2", color="info", pill=True, style={"margin-left": "1rem"}),
		# Right part:
		# dbc.Container(
		# 	children=[
		# 		# Cumulative density function
		# 		# ,
		# 		# ,
		# 	],
		# 	style={
		# 		"width": "29%",
		# 		"height": "85vh",
		# 		"margin-left": "70%",
		# 		"margin-top": "-100vh",
		# 		"display": "inline-block",
		# 	},
		# )
	],
	style={
		"width": "90%",
		"height": "100vh",
		"margin-left": "10%",
		"margin-top": "-100vh",
		# "display": "inline-block",
	}
)
