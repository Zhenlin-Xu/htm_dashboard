import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import dash_leaflet as dl
import plotly.express as px

from data_process.data import *

# NUMBERS
round_rectangles = html.Div(
	children=[
		html.Div(
			[
				html.P("Overall overspeeding"),
				html.P(f"{len(overspeed)}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
		html.Div(
			[
				html.P("Straight overspeeding"),
				html.P(f"{len(straight_overspeed)}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
		html.Div(
			[
				html.P("Turning overspeeding"),
				html.P(f"{len(turning_overspeed)}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
		html.Div(
			[
				html.P("Percentage of overspeeding"),
				html.P(f"{len(overspeed) / len(speed):.2f}"),
				html.P("in 2023"),
			],
			className="round_rectangle",
		),
	],
	className="round_rectangles"
)

# MAPS
geographic_map = dl.Map(
		children=[
			dl.TileLayer(),
			*[
				dl.CircleMarker(
					center=[52.08, 4.30],
					radius=100,
					color="red",
				)
			]
		],
		center=[52.08, 4.30],
		zoom=13,
		style={
			# size
			"height": "50vh",
			"width": "100%",
		},
	)


# HISTOGRAM
# @callback(
# 	[Output("speed_distribution_figure", "figure")],
# 	[Input("useless", "style")]
# )
# def gen_speed_distribution_histogram(useless):
# 	data_frame = speed[["speed", "line", "is_straight"]]
# 	data_frame = data_frame.groupby(["is_straight", "speed"]).count()
# 	data_frame.reset_index(inplace=True)
# 	speed_distribution_figure = px.histogram(
# 		data_frame, x="speed", y="line",
# 		color="is_straight",
# 		nbins=len(data_frame["speed"].unique()),
# 		title="The speed distribution"
# 	)
# 	speed_distribution_figure.add_vline(x=15, line_color="red", line_width=2)
# 	speed_distribution_figure.update_layout(
# 		legend=dict(x=0.9, y=0.99),
# 		title=dict(x=0.05, y=0.92),
# 		margin=dict(l=0, r=0, b=0, t=35)
# 	)
# 	return [speed_distribution_figure, ]
#
#
# speed_distribution_figure = dcc.Graph(
# 	id="speed_distribution_figure",
# 	style={
# 		"width": "20vw",
# 		"height": "16vh",
# 		"margin-left": "22vw",
# 		"margin-top": "-66vh",
# 		"padding": "0.2rem",
# 		"background-color": "rgb(255, 255, 25)"
# 	},
# )

# TODO: TABLE

overview_layout = dbc.Container(
	children=[
		html.H2("Overspeeding dashboard"),
		html.H4([dbc.Badge("Overview", color="danger", pill=True)]),
		html.Hr(id="useless"),
		# round_rectangles,
		geographic_map,
		# speed_distribution_figure,
	],
)
