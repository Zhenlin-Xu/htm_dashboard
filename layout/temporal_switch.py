import pandas as pd
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from data_process.data import (
	speed, overspeed, straight_overspeed, turning_overspeed,
)


# HEATMAP
@callback([Output("heatmap_switch", "figure")], [
		Input("switch_input", "value"),
		Input("switch_type_input", "value")])
def gen_temporal_tramline_heatmap(switch_input, switch_type_input):
	data_frame = None
	if switch_type_input == "overall":
		data_frame = overspeed
	elif switch_type_input == "straight":
		data_frame = straight_overspeed
	elif switch_type_input == "turning":
		data_frame = turning_overspeed

	# filter the specific tramline
	switch = data_frame[data_frame["switch_number"] == switch_input]
	# select the specific columns
	switch = switch[["switch_number", "#week", "#day"]]
	# groupby operation
	switch = switch.groupby(["#week", "#day"]).count()
	# concatenation operation
	switch = pd.concat([switch, switch.index.to_frame()], axis=1)
	# pivot operation
	switch = switch.pivot(columns="#week", index="#day", values="switch_number")
	# draw the heatmap
	heatmap = px.imshow(
		img=switch, x=switch.columns, y=switch.index,
		color_continuous_scale="reds",
		range_color=[0, 500],
		title=f"The temporal distribution of {switch_type_input} over-speeding for switch {switch_input}.", )
	# specify the layout details
	heatmap.update_layout(
		coloraxis_colorbar=dict(len=0.5),
		margin=dict(t=10, b=0, ),
		title=dict(x=0.05, y=0.9),
		xaxis_title="#Week", yaxis_title="#Day",
		yaxis=dict(tickmode="linear", range=[1, 7], dtick=1),
		xaxis=dict(tickmode="linear", range=[1, 55], dtick=2),
	)
	return [heatmap, ]


# HISTOGRAM
@callback([Output("histogram_switch", "figure")], [
	Input("switch_input", "value"),
	Input("switch_logy_button", "value")])
def gen_temporal_tramline_histogram(switch_input, switch_logy_button):
	tramline_month_speed = speed[speed["switch_number"] == switch_input]
	tramline_month_speed['is_straight'] = tramline_month_speed['is_straight'].map({True: 'Straight', False: 'Turning'}).astype(str)
	tramline_month_speed = tramline_month_speed[["switch_number", "speed", "is_straight", "month"]].groupby(
		["is_straight", "month", "speed"]).count()
	tramline_month_speed.reset_index(inplace=True)
	histogram = px.histogram(
		data_frame=tramline_month_speed,
		x="speed",
		y="switch_number",
		color="is_straight",
		animation_frame="month",
		nbins=55,
		log_y=True if switch_logy_button == "log" else False,
		# height=400,
	)
	# add the speed limit vertical line.
	histogram.add_vline(x=15, line_color="yellow", line_width=2)
	# adjust the position of the legend.
	histogram.update_layout(
		legend=dict(title="Type", x=0.9, y=0.99),
		title=dict(text=f"Histogram of monthly speed distribution of tramline {switch_input}."),
		xaxis_title="Speed",
		yaxis_title="#overspeed records",
		xaxis=dict(tickmode="linear", range=[1, 55], dtick=2),
	)
	return [histogram, ]


@callback(
	[Output("temporal_switch_response", "children"),
	 Output("temporal_switch_response2", "children")],
	[Input("switch_input", "value"),
	Input("switch_type_input", "value"),
	Input("switch_logy_button", "value"),])
def temporal_switch_response(switch_input, switch_type_input, switch_logy_button):
	logy_button = "" if switch_logy_button == "log" else "not"
	return [f"Hello, you have selected switch {switch_input} and {switch_type_input} overspeed for inspection.",
			f"Hello, you have selected switch {switch_input} and the histogram's y-axis is {logy_button} in log-scale."]


switch_input = dcc.Dropdown(
	options=overspeed["switch_number"].unique(),
	value="W127",
	id="switch_input",
	# placeholder="Select a switch",
	style={"width": "5rem", "display": "inline-block", "margin-left": "1rem"})

type_input = dcc.Dropdown(
	options=["overall", "straight", "turning"],
	value="overall",
	id="switch_type_input",
	# placeholder="Select the type of overspeed",
	style={"width": "8rem", "display": "inline-block", "margin-left": "1rem"})

logY_button = dbc.RadioItems(
	options=["linear", "log"],
	value="linear",
	id="switch_logy_button",
	inline=True,
	style={
		"display": "inline-block",
		"margin-left": "1rem",
	}
)

heatmap_switch = dcc.Graph(
	id="heatmap_switch",
	style={"height": "30vh"},
)
histogram_switch = dcc.Graph(
	id="histogram_switch",
	style={"height": "40vh"}
)

temporal_switch_layout = html.Div(
	children=[
		# Header:
		dbc.Container(
			[
				html.H2("Temporal analysis"),
				html.H4([dbc.Badge("Switch", color="danger", pill=True)]),
			],
			style={"padding": "0.3rem"}
		),
		html.Hr(),
		dbc.Container(
			children=[
				html.P(html.B("#Switch:"), style={"margin-left": "2rem", "display": "inline-block", }),
				switch_input,
				html.P(html.B("Overspeed type:"), style={"margin-left": "2rem", "display": "inline-block", }),
				type_input,
			],
			style={"display": "inline-block"}
		),
		heatmap_switch,
		dbc.Badge(
			color="info",
			pill=True,
			id="temporal_switch_response",
			style={
				"display": "inline-block",
				"margin-left": "2rem",
				"font-size": "small",
			},
		),
		# bottom part:
		html.Hr(),
		dbc.Container(
			children=[
				html.P(html.B("Y axis:"), style={"margin-left": "2rem", "display": "inline-block", }),
				logY_button,
			]
		),
		histogram_switch,
		dbc.Badge(
			color="info",
			pill=True,
			id="temporal_switch_response2",
			style={
				"display": "inline-block",
				"margin-left": "2rem",
				"font-size": "small",
			}
		),
	],
	style={
		"width": "90%",
		"height": "100vh",
		"margin-left": "10%",
		"margin-top": "-100vh",
		# "display": "inline-block",
	}
)
