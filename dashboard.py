import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

from layout import sidebar_layout
from layout import overview_layout
from layout import spatial_switch_layout
from layout import spatial_tramline_layout
from layout import temporal_switch_layout
from layout import temporal_tramline_layout


app = dash.Dash(
	name=__name__,
	external_stylesheets=[dbc.themes.UNITED],
	suppress_callback_exceptions=True,
)

content = dbc.Container(id="content")
app.layout = dbc.Container(
	children=[
		dcc.Location(id="url"),
		# sidebar_layout,
		content,
	],
	className="container",
	fluid=True,
)


@app.callback(
	Output("content", "children"),
	Input("url", "pathname"))
def render_content(pathname):
	"""
	The callback function that selects the content through the sidebar.

	:param pathname: the url of the navlink points to.
	:return: the content that the navlink points to.
	"""
	if pathname == "/":
		return overview_layout
	elif pathname == "/spatial_tramline":
		return spatial_tramline_layout
	elif pathname == "/spatial_switch":
		return spatial_switch_layout
	elif pathname == "/temporal_tramline":
		return temporal_tramline_layout
	elif pathname == "/temporal_switch":
		return temporal_switch_layout


if __name__ == "__main__":
	app.run_server(debug=True, port=10001)
