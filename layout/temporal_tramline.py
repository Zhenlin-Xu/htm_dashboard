import pandas as pd
from dash import html, dcc, callback, Input, Output
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
		xaxis_title="#Week", yaxis_title="#Day",
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
	tramline_month_speed['is_straight'] = tramline_month_speed['is_straight'].map({True: 'Straight', False: 'Turning'}).astype(str)
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
		log_y=True if tramline_logy_button == "log" else False,
		# labels={
		# 	"is_straight": ["Straight", "Turning"],
		# }
		# height=400,
	)
	# current_frame_index = int(histogram_tramline * (len(histogram.frames) - 1))
	# add the speed limit vertical line.
	histogram.add_vline(x=15, line_color="yellow", line_width=2)
	# adjust the position of the legend.
	histogram.update_layout(
		legend=dict(x=0.9, y=0.99, title="Type"),
		title=dict(text=f"Histogram of monthly speed distribution of tramline {tramline_input}."),
		xaxis_title="Speed",
		yaxis_title="#Overspeed records",
		xaxis=dict(tickmode="linear", range=[1, 55], dtick=2),
	)
	return [histogram, ]


@callback([
	Output("temporal_tramline_response", "children"),
	Output("temporal_tramline_response2", "children"),
], [
	Input("tramline_input", "value"),
	Input("tramline_type_input", "value"),
	Input("tramline_logy_button", "value"),
])
def temporal_tramline_response(tramline_input, tramline_type_input, tramline_logy_button):
	logy_button = "" if tramline_logy_button == "log" else "not"
	return [
		f"Hello, you have selected tramline {tramline_input} and {tramline_type_input} overspeed for inspection.",
		f"Hello, you have selected tramline {tramline_input} and the histogram's y-axis is {logy_button} in log-scale."
	]


tramline_input = dcc.Dropdown(
	options=overspeed["line"].unique(), value=1, id="tramline_input",
	style={"width": "5rem", "margin-left": "1rem", "display": "inline-block"})
type_input = dcc.Dropdown(
	options=["overall", "straight", "turning"],
	value="overall",
	id="tramline_type_input",
	style={"width": "10rem", "display": "inline-block", "margin-left": "1rem"})
heatmap_tramline = dcc.Graph(
	id="heatmap_tramline",
	style={"height": "30vh"}
)
logY_button = dbc.RadioItems(
	options=["linear", "log"],
	value="linear",
	id="tramline_logy_button",
	inline=True,
	style={
		"display": "inline-block",
		"margin-left": "1rem",
	}
)
histogram_tramline = dcc.Graph(
	id="histogram_tramline",
	style={"height": "40vh"}
)

temporal_tramline_layout = html.Div(
	children=[
		# Header:
		dbc.Container(
			[
				html.H2("Temporal analysis"),
				html.H4([dbc.Badge("Tramline", color="danger", pill=True)]),
			],
			style={"padding": "0.3rem"}
		),
		html.Hr(),
		dbc.Container(children=[
			html.P(html.B("#Tramline:"), style={"margin-left": "2rem", "display": "inline-block",}),
			tramline_input,
			html.P(html.B("Overspeed type:"), style={"margin-left": "2rem", "display": "inline-block", }),
			type_input,
		], style={"display": "inline-block"}),
		heatmap_tramline,
		dbc.Badge(
			color="info",
			pill=True,
			id="temporal_tramline_response",
			style={
				"display": "inline-block",
				"margin-left": "2rem",
				"font-size": "small",
			}
		),
		html.Hr(),
		# Bottom part:
		dbc.Container(children=[
			html.P(html.B("Y axis:"), style={"margin-left": "2rem", "display": "inline-block", }),
			logY_button,
		]),
		histogram_tramline,
		dbc.Badge(
			color="info",
			pill=True,
			id="temporal_tramline_response2",
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
