import pandas as pd
from dash import html, dcc, callback, Input, Output
import dash_daq as daq
import plotly.express as px

from data_process.data import (
	speed, overspeed, straight_overspeed, turning_overspeed,
	straight_temporal_tramline_grpby
)


# HEATMAP
@callback([Output("heatmap_str", "figure"),
		   Output("heatmap_trn", "figure"), ],
		  [Input("tramline_input", "value"), ])
def gen_temporal_tramline_heatmap(tramline_input):
	# filter the specific tramline
	straight_tramline = straight_overspeed[straight_overspeed["line"] == tramline_input]
	turning_tramline = turning_overspeed[turning_overspeed["line"] == tramline_input]
	# select the specific columns
	straight_tramline = straight_tramline[["line", "#week", "#day"]]
	turning_tramline = turning_tramline[["line", "#week", "#day"]]
	# groupby operation
	straight_tramline = straight_tramline.groupby(["#week", "#day"]).count()
	turning_tramline = turning_tramline.groupby(["#week", "#day"]).count()
	# concatenation operation
	straight_tramline = pd.concat([straight_tramline, straight_tramline.index.to_frame()], axis=1)
	turning_tramline = pd.concat([turning_tramline, turning_tramline.index.to_frame()], axis=1)
	# pivot operation
	straight_tramline = straight_tramline.pivot(columns="#week", index="#day", values="line")
	turning_tramline = turning_tramline.pivot(columns="#week", index="#day", values="line")
	# draw the heatmap
	heatmap_str = px.imshow(
		img=straight_tramline,
		x=straight_tramline.columns,
		y=straight_tramline.index,
		title=f"The temporal distribution of straight over-speeding for tramline {tramline_input}."
	)
	heatmap_trn = px.imshow(
		img=turning_tramline,
		x=turning_tramline.columns,
		y=turning_tramline.index,
		title=f"The temporal distribution of turning over-speeding for tramline {tramline_input}."
	)
	# specify the layout details
	heatmap_str.update_layout(
		coloraxis_colorbar=dict(orientation="v", len=0.65),
		margin=dict(t=10, b=0,),
		title=dict(x=0.05, y=0.9)
	)
	heatmap_trn.update_layout(
		coloraxis_colorbar=dict(orientation="v", len=0.65),
		margin=dict(t=10, b=0,),
		title=dict(x=0.05, y=0.9)
	)
	return [heatmap_str, heatmap_trn]


# HISTOGRAM
@callback([Output("histogram_month_speed", "figure"),],
		   [Input("tramline_input", "value"),
		    Input("logy_button", "value")])
def gen_temporal_tramline_histogram(tramline_input, logy_button):
	tramline_month_speed = speed[["line", "speed", "is_straight", "month"]].groupby(
		["is_straight", "month", "speed"]).count()
	tramline_month_speed.reset_index(inplace=True)

	histogram = px.histogram(
		data_frame=tramline_month_speed,
		x="speed",
		y="line",
		color="is_straight",
		animation_frame="month",
		nbins=len(tramline_month_speed["speed"].unique()),
		log_y=logy_button, # TODO: add a button to toggle log_y or not.
		title=f"The histogram of speed distribution for tramline {tramline_input}.",
		height=500,
	)
	histogram.add_vline(x=15, line_color="red", line_width=2)
	return [histogram,]


tramline_input = dcc.Dropdown(options=overspeed["line"].unique(), value=1, id="tramline_input")
heatmap_str = dcc.Graph(id="heatmap_str", className="heatmap")
heatmap_trn = dcc.Graph(id="heatmap_trn", className="heatmap")
logY_button = daq.ToggleSwitch(
	id="logy_button", value=False, label="Log y", labelPosition='right', size=50,
	color="red", style={"width": "5vw"}
)
histogram_month_speed = dcc.Graph(id="histogram_month_speed", className="histogram_month_speed")

temporal_tramline_layout = html.Div(
	children=[
		html.H2("Temporal analysis"),
		html.H4("Tramline"),
		html.Hr(),
		tramline_input,
		html.Hr(),
		heatmap_str,
		html.Hr(),
		heatmap_trn,
		html.Hr(),
		logY_button,
		histogram_month_speed,
	],
	className="content_container",
)
