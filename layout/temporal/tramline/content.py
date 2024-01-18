import pandas as pd
from dash import html, dcc, callback, Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px

from data_process.data import (
	speed, overspeed, straight_overspeed, turning_overspeed,
)


# HEATMAP
@callback([Output("heatmap_tramline", "figure")], [
		Input("tramline_input", "value"),
		Input("tramline_type_input", "value")])
def gen_temporal_tramline_heatmap(tramline_input, tramline_type_input):
	data_frame = None
	if tramline_type_input == "overall":
		data_frame = overspeed
	elif tramline_type_input == "straight":
		data_frame = straight_overspeed
	elif tramline_type_input == "turning":
		data_frame = turning_overspeed

	# filter the specific tramline
	tramline = data_frame[data_frame["line"] == tramline_input]
	# select the specific columns
	tramline = tramline[["line", "#week", "#day"]]
	# groupby operation
	tramline = tramline.groupby(["#week", "#day"]).count()
	# concatenation operation
	tramline = pd.concat([tramline, tramline.index.to_frame()], axis=1)
	# pivot operation
	tramline = tramline.pivot(columns="#week", index="#day", values="line")
	# draw the heatmap
	heatmap = px.imshow(
		img=tramline, x=tramline.columns, y=tramline.index, color_continuous_scale="reds",
		title=f"The temporal distribution of {tramline_type_input} over-speeding for tramline {tramline_input}.", )
	# specify the layout details
	heatmap.update_layout(
		coloraxis_colorbar=dict(orientation="v", len=0.75),
		margin=dict(t=10, b=0, ),
		title=dict(x=0.05, y=0.9)
	)
	return [heatmap, ]


# HISTOGRAM
@callback([Output("histogram_tramline", "figure")], [
		Input("tramline_input", "value"),
		Input("tramline_logy_button", "value")],
		suppress_callback_exceptions=True)
def gen_temporal_tramline_histogram(tramline_input, tramline_logy_button):
	tramline_month_speed = speed[speed["line"] == tramline_input]
	tramline_month_speed = tramline_month_speed[["line", "speed", "is_straight", "month"]].groupby(
		["is_straight", "month", "speed"]).count()
	tramline_month_speed.reset_index(inplace=True)
	histogram = px.histogram(
		data_frame=tramline_month_speed,
		x="speed",
		y="line",
		color="is_straight",
		animation_frame="month",
		nbins=len(tramline_month_speed["speed"].unique()),
		log_y=tramline_logy_button,
		height=500,
	)
	# current_frame_index = int(histogram_tramline * (len(histogram.frames) - 1))
	# add the speed limit vertical line.
	histogram.add_vline(x=15, line_color="red", line_width=2)
	# adjust the position of the legend.
	histogram.update_layout(
		legend=dict(x=0.9, y=0.99),
		title=dict(text=f"The histogram of speed distribution in for tramline {tramline_input}."),
	)
	return [histogram, ]


tramline_input = dcc.Dropdown(
	options=overspeed["line"].unique(), value=1, id="tramline_input",
	style={"width": "20vw", "display": "inline-block"})
type_input = dcc.Dropdown(
	options=["overall", "straight", "turning"], value="overall", id="tramline_type_input",
	style={"width": "20vw", "display": "inline-block", "margin-left": "3rem"})
heatmap_tramline = dcc.Graph(id="heatmap_tramline", className="heatmap")
logY_button = daq.ToggleSwitch(
	id="tramline_logy_button", value=False, label="Log y", labelPosition='right', size=50,
	color="red", style={"width": "5vw"})
histogram_tramline = dcc.Graph(
	id="histogram_tramline",
	className="histogram_month_speed")

temporal_tramline_layout = html.Div(
	children=[
		html.H2("Temporal analysis"),
		html.H4("Tramline"),
		html.Hr(),
		dbc.Container(children=[tramline_input, type_input], style={"display": "inline-block"}),
		heatmap_tramline,
		html.Hr(),
		logY_button,
		histogram_tramline,
	],
	className="content_container",
)

# TODO: calculate the percentage of over-speeding
