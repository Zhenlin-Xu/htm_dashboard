import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import plotly.express as px

from data_process.data import *


# HISTOGRAM
# groupby operation

@callback(
	Output("speed_distribution_figure", "figure"),
	Input("overview_logy_button", "value")
)
def gen_overview_speed_distribution(overview_logy_button):
	data_frame = speed[["speed", "line", "is_straight"]]
	data_frame['is_straight'] = data_frame['is_straight'].map({True: 'Straight', False: 'Turning'}).astype(str)
	data_frame = data_frame.groupby(["is_straight", "speed"]).count()
	data_frame.reset_index(inplace=True)
	# draw the histogram
	speed_distribution_figure = px.histogram(
		data_frame, x="speed", y="line",
		color="is_straight",
		log_y=True if overview_logy_button == "log" else False,
		nbins=len(data_frame["speed"].unique()),
		color_discrete_map={"Straight": "red", "Turning": "blue"},
		# template="ggplot2",
	)
	# draw the vertical line of the speed limit 15 km/h
	speed_distribution_figure.add_vline(x=15, line_color="yellow", line_width=3)
	speed_distribution_figure.update_layout(
		xaxis_title="Speed (km/h)",
		yaxis_title="#Overspeed records",
		# title="The speed distribution",
		legend=dict(title="Type", x=0.925, y=1),
		margin=dict(l=0, r=0, t=0, b=0),
		xaxis=dict(tickmode="linear", range=[1, len(data_frame["speed"].unique())], dtick=1),
	)
	return speed_distribution_figure


speed_distribution_figure = dcc.Graph(
	id="speed_distribution_figure",
	style={
		"height": "20vh",
		"width": "100%",
		# "margin-left": "51%",
		# "margin-top": "-69vh",
		# "display": "inline-block",
		"padding": "0.1rem",
		# "background-color": "rgb(255, 255, 25)"
	},
)

# MAPS
# Left
# groupby operation
zoom, lat, lon = 11.5, 52.06, 4.32
data_frame = straight_overspeed[["switch_number", "latitude", "longitude", "speed", ]]
data_frame = data_frame.groupby(["switch_number", "latitude", "longitude"]).count()
data_frame.reset_index(inplace=True)
# draw background map and markers
geographic_map_str = dl.Map(
	children=[
		dl.TileLayer(),
		*[dl.CircleMarker(
			center=[row["latitude"], row["longitude"]],
			radius=row["speed"] / 5000,
			color="red") for _, row in data_frame.iterrows()],
	],
	center=[lat, lon], zoom=zoom,
	style={
		# size
		"height": "30vh",
		"width": "49%",
		"padding": "1rem",
		"display": "inline-block",
		"border-radius": "15px",
	},
)
# sort in the descending order
data_frame = data_frame.sort_values(by="speed", ascending=False)
data_frame = data_frame[["switch_number", "speed"]]
data_frame.columns = ["#switch", "#overspeed records"]
data_frame = data_frame.iloc[:10]
# reshape
data_frame["Rank"] = [i for i in range(1, 11)]
half_rows = len(data_frame) // 2
df_first_half = data_frame.iloc[:half_rows]
df_second_half = data_frame.iloc[half_rows:]
df_first_half.reset_index(drop=True, inplace=True)
df_second_half.reset_index(drop=True, inplace=True)
df_concatenated = pd.concat([df_first_half, df_second_half], axis=1)
df_concatenated.columns = ['#switch', '#overspeed records', 'Rank', '#switch', '#overspeed records', 'Rank']

top10_str_table = dbc.Table.from_dataframe(
	df=df_concatenated, striped=True, bordered=True, hover=True, color="danger",
	style={"width": "49%", "height": "15vh", "display": "inline-block"}
)
# Right
# groupby operation
data_frame = turning_overspeed[["switch_number", "latitude", "longitude", "speed", ]]
data_frame = data_frame.groupby(["switch_number", "latitude", "longitude"]).count()
data_frame.reset_index(inplace=True)
# draw background map and markers
geographic_map_trn = dl.Map(
	children=[
		dl.TileLayer(),
		*[dl.CircleMarker(
			center=[row["latitude"], row["longitude"]],
			radius=row["speed"] / 5000,
			color="blue") for _, row in data_frame.iterrows()]
	],
	center=[lat, lon], zoom=zoom,
	style={
		# size
		"height": "30vh",
		"width": "49%",
		"padding": "1rem",
		"margin-left": "2%",
		"display": "inline-block",
		"border-radius": "15px",
	},
)
# sort in the descending order
data_frame = data_frame.sort_values(by="speed", ascending=False)
data_frame = data_frame[["switch_number", "speed"]]
data_frame.columns = ["#switch", "#overspeed records"]
data_frame = data_frame.iloc[:10]
# reshape
data_frame["Rank"] = [i for i in range(1, 11)]
half_rows = len(data_frame) // 2
df_first_half = data_frame.iloc[:half_rows]
df_second_half = data_frame.iloc[half_rows:]
df_first_half.reset_index(drop=True, inplace=True)
df_second_half.reset_index(drop=True, inplace=True)
df_concatenated = pd.concat([df_first_half, df_second_half], axis=1)
df_concatenated.columns = ['#switch', '#overspeed records', 'Rank', '#switch', '#overspeed records', 'Rank']

top10_trn_table = dbc.Table.from_dataframe(
	df=df_concatenated, striped=True, bordered=True, hover=True, color="info",
	style={"width": "49%", "height": "15vh", "display": "inline-block", "margin-left": "2%"}
)


@callback(
	Output("overview_response", "children"),
	Input("overview_logy_button", "value")
)
def overview_response(overview_logy_button):
	return f"""
		Hello, the histogram's y-axis is in {overview_logy_button} scaled now.
	"""


overview_layout = dbc.Container(
	children=[
		html.H1("Dashboard Overview", style={"text-align": "center"}),
		# Important numbers in the badges:
		html.H3([
			dbc.Badge(
				children=f"""
					#overspeed records: {overspeed.shape[0]:,} ({(overspeed.shape[0] / speed.shape[0]) * 100:.1f}%)
					""",
				color="danger", pill=True,
				style={"font-size": "Large"}),
			dbc.Badge(
				children=f"""
					#straight overspeed records: {straight_overspeed.shape[0]:,} ({(straight_overspeed.shape[0] / straight_speed) * 100:.1f}%)
					""",
				color="success", pill=True,
				style={"font-size": "Large", "margin-left": "1rem"}),
			dbc.Badge(
				children=f"""
					#turning overspeed records: {turning_overspeed.shape[0]:,} ({(turning_overspeed.shape[0] / turning_speed) * 100:.1f}%)
					""",
				color="info", pill=True,
				style={"font-size": "Large", "margin-left": "1rem"}),
		]
		),
		html.Hr(id="useless"),
		# Speed distribution histogram:
		dbc.Container(children=[
			html.H3("Speed distribution histogram:", style={"display": "inline-block"}),
			dbc.RadioItems(
				id="overview_logy_button",
				options=["linear", "log"],
				value="linear",
				inline=True,
				style={
					"display": "inline-block",
					"margin-left": "1rem",
				}, ),
			dbc.Badge(
				id="overview_response",
				color="primary",
				pill=True,
				style={
					"display": "inline-block",
					"margin-left": "2rem",
					"font-size": "medium"
				},
			),
		]),
		speed_distribution_figure,
		html.Hr(),
		# Map:
		html.H3("Maps of HTM tram network:"),
		geographic_map_str, geographic_map_trn,
		dbc.Badge(
			children="Straight overspeed", color="danger", pill=True,
			style={"text-align": "left", "margin-left": "-1rem", "font-size": "small", "display": "inline-block"}),
		dbc.Badge(
			children="Turning overspeed", color="info", pill=True,
			style={"margin-left": "40%", "font-size": "small", "display": "inline-block"}),
		html.Hr(),
		# Top-10 tables:
		html.H3("Top-10 tables:"),
		top10_str_table, top10_trn_table,
		dbc.Badge(
			children="Straight overspeed", color="danger", pill=True,
			style={
				"margin-top": "2rem",
				"text-align": "left", "margin-left": "-1rem", "font-size": "small", "display": "inline-block"}),
		dbc.Badge(
			children="Turning overspeed", color="info", pill=True,
			style={"margin-left": "40%", "font-size": "small", "display": "inline-block"}),
	],
)
