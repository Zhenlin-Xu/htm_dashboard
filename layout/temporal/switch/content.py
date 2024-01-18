import pandas as pd
from dash import html, dcc, callback, Input, Output
import dash_daq as daq
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
		img=switch, x=switch.columns, y=switch.index, color_continuous_scale="reds",
		title=f"The temporal distribution of {switch_type_input} over-speeding for switch {switch_input}.", )
	# specify the layout details
	heatmap.update_layout(
		coloraxis_colorbar=dict(orientation="v", len=0.75),
		margin=dict(t=10, b=0, ),
		title=dict(x=0.05, y=0.9)
	)
	return [heatmap, ]


# HISTOGRAM
@callback([Output("histogram_switch", "figure")], [
	Input("switch_input", "value"),
	Input("switch_logy_button", "value")])
def gen_temporal_tramline_histogram(switch_input, switch_logy_button):
	tramline_month_speed = speed[speed["switch_number"] == switch_input]
	tramline_month_speed = tramline_month_speed[["switch_number", "speed", "is_straight", "month"]].groupby(
		["is_straight", "month", "speed"]).count()
	tramline_month_speed.reset_index(inplace=True)
	histogram = px.histogram(
		data_frame=tramline_month_speed,
		x="speed",
		y="switch_number",
		color="is_straight",
		animation_frame="month",
		nbins=len(tramline_month_speed["speed"].unique()),
		log_y=switch_logy_button,
		height=500,
	)
	# add the speed limit vertical line.
	histogram.add_vline(x=15, line_color="red", line_width=2)
	# adjust the position of the legend.
	histogram.update_layout(
		legend=dict(x=0.9, y=0.99),
		title=dict(text=f"The histogram of speed distribution in for switch {switch_input}."),
	)
	return [histogram, ]


switch_input = dcc.Dropdown(
	options=overspeed["switch_number"].unique(),
	value="W127",
	id="switch_input",
	style={"width": "20vw", "display": "inline-block"})
type_input = dcc.Dropdown(
	options=["overall", "straight", "turning"],
	value="overall",
	id="switch_type_input",
	style={"width": "20vw", "display": "inline-block", "margin-left": "3rem"})
heatmap_switch = dcc.Graph(
	id="heatmap_switch",
	className="heatmap")
logY_button = daq.ToggleSwitch(
	id="switch_logy_button", value=False, label="Log y", labelPosition='right', size=50,
	color="red", style={"width": "5vw"})
histogram_switch = dcc.Graph(
	id="histogram_switch",
	className="histogram_month_speed")

temporal_switch_layout = html.Div(
	children=[
		html.H2("Temporal analysis"),
		html.H4("Switch"),
		html.Hr(),
		dbc.Container(children=[switch_input, type_input], style={"display": "inline-block"}),
		heatmap_switch,
		html.Hr(),
		logY_button,
		histogram_switch,
	],
	className="content_container",
)
