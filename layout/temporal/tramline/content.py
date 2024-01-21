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
		img=tramline, x=tramline.columns, y=tramline.index,
		color_continuous_scale="reds",
		range_color=[0, 1500],
		title=f"The temporal distribution of {tramline_type_input} over-speeding for tramline {tramline_input}.", )
	# specify the layout details
	heatmap.update_layout(
		coloraxis_colorbar=dict(len=0.5),
		margin=dict(t=10, b=0, ),
		title=dict(x=0.05, y=0.9),
		yaxis=dict(tickmode="linear", range=[1, 7], dtick=1),
		xaxis=dict(tickmode="linear", range=[1, 55], dtick=2),
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
		nbins=55,
		log_y=tramline_logy_button,
		# height=400,
	)
	# current_frame_index = int(histogram_tramline * (len(histogram.frames) - 1))
	# add the speed limit vertical line.
	histogram.add_vline(x=15, line_color="yellow", line_width=2)
	# adjust the position of the legend.
	histogram.update_layout(
		legend=dict(x=0.9, y=0.99),
		title=dict(text=f"Histogram of monthly speed distribution of tramline {tramline_input}."),
		xaxis_title="speed",
		yaxis_title="#overspeed records",
		xaxis=dict(tickmode="linear", range=[1, 55], dtick=2),
	)
	return [histogram, ]


@callback(
	[Output("temporal_tramline_response", "children"),
	 Output("temporal_tramline_response2", "children")],
	[Input("tramline_input", "value"),
	 Input("tramline_type_input", "value"),
	 Input("tramline_logy_button", "value"),])
def temporal_tramline_response(tramline_input, tramline_type_input, tramline_logy_button):
	logy_button = "" if tramline_logy_button else "not"
	return [f"Hello, you have selected tramline {tramline_input} and {tramline_type_input} overspeed for inspection.",
			f"Hello, you have selected tramline {tramline_input} and the histogram's y-axis is {logy_button} in log-scale."]


tramline_input = dcc.Dropdown(
	options=overspeed["line"].unique(), value=1, id="tramline_input",
	style={"width": "5rem", "display": "inline-block"})
type_input = dcc.Dropdown(
	options=["overall", "straight", "turning"],
	value="overall",
	id="tramline_type_input",
	style={"width": "10rem", "display": "inline-block", "margin-left": "1rem"})
heatmap_tramline = dcc.Graph(
	id="heatmap_tramline",
	style={"height": "30vh"}
)
logY_button = daq.ToggleSwitch(
	id="tramline_logy_button", value=False, label="log-y", labelPosition='right', size=50,
	color="red", style={"margin-left": "1rem", "margin-top": "-1rem", "height": "2rem", "display": "inline-block", })
histogram_tramline = dcc.Graph(
	id="histogram_tramline",
	style={"height": "45vh"}
)

temporal_tramline_layout = html.Div(
	children=[
		html.H2("Temporal analysis "),
		html.H4([dbc.Badge("Tramline", color="danger", pill=True)]),
		html.Hr(),
		dbc.Container(children=[
			tramline_input,
			type_input,
			html.Div(id="temporal_tramline_response", style={"display": "inline-block", "margin-left": "2rem",}),
		], style={"display": "inline-block"}),
		heatmap_tramline,
		html.Hr(),
		dbc.Container(children=[
			logY_button,
			html.Div(id="temporal_tramline_response2", style={"display": "inline-block", "margin-left": "2rem",}),
		]),
		histogram_tramline,
	],
	className="content_container",
)
