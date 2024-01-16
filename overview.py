from dash import html, dcc, dash_table
import dash_leaflet as dl
import plotly.express as px

from data import *

# top-left corner
ROUNDRECTANGLE_STYLE = {
    "width": "9rem",
    "height": "10rem",
    "margin-left": "1rem",
    "padding": "1rem",
    "background-color": "#f2f9fa",
    "display": "inline-block"
}
round_rectangles = html.Div(
    children=[
        html.Div(
            children=[
                html.P("Overall overspeeding"),
                html.H3(f"{len(overspeed)}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE
        ),
        html.Div(
            children=[
                html.P("Straight overspeeding"),
                html.H3(f"{len(straight_overspeed)}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE
        ),
        html.Div(
            children=[
                html.P("Turning overspeeding"),
                html.H3(f"{len(turning_overspeed)}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE,
        ),
        html.Div(
            children=[
                html.P("% of overspeeding"),
                html.H3(f"{len(overspeed)/len(speed):.2f}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE,
        ),
    ],
)

# middle-left: map
# https://www.dash-leaflet.com
OVERVIEW_MAP_STYLE = {
    "position": "fixed",
    "width": "80rem",
}
overview_map_figure = dl.Map(
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
    style={'height': '60vh'}
)
#     px.scatter_geo(
#     data_frame=data.query("year == 2027"),
#     locations="iso_alpha",
#     size="pop",
#     width=600,
#     height=400,
#     title="The spatial distribution of the switch",
# )
overview_map = html.Div(
    overview_map_figure,
    style={"margin-top": "1rem"},
)

# # bottom-left corner
# overview_heatmap_figure = px.imshow(
#     img=[
#         [1, 20, 30],
#         [20, 1, 60],
#     ],
#     title="The temporal distribution of overspeeding",
#     width=600,
#     height=400,
# )
# overview_heatmap = html.Div(
#     children=[
#         dcc.Graph(
#             figure=overview_heatmap_figure
#         ),
#     ],
#     style={"margin-top": "1rem"}
# )

# top-right corner: distribution histogram
overview_histogram_figure = px.histogram(
    number_records_per_speed,
    x=number_records_per_speed.index,
    y="line",
    nbins=len(number_records_per_speed.index),
    color="is_straight",
    title="The distribution of tram speed in 2023",
    labels={"line": "speed records",},
    log_y=True,
)
overview_histogram_figure.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99),
    margin=dict(l=10, r=0, b=0, t=25)
)
overview_histogram_figure.add_vline(
    x=SPEED_LIMIT + 0.5,
    line_color="red",
    line_width=5)
overview_histogram = html.Div(
    children=[
        dcc.Graph(
            figure=overview_histogram_figure
        ),
    ],
    style={
        "margin-top": "1rem",
        "width": "50rem",
        "height": "20rem",
    }
)

# bottom-right corner: top-N table
# TODO: 2 row-header: https://dash.plotly.com/datatable/style
overview_topN_table = html.Div(
    children=[
        dash_table.DataTable(
            data=number_overspeed_records_per_switch.to_dict("records"),
            columns=[{'id': c, 'name': c}
                for c in number_overspeed_records_per_switch.columns],
            page_size=10,
        )
    ],
    style={"margin-top": "10rem", "width": "50rem"}
)

OVERVIEW_LEFT_STYLE = {
    "position": "fixed",
    "width": "42rem",
    "padding": "1rem",
    "background-color": "#f8f9fa",
}
overview_left = html.Div(
    children=[
        round_rectangles,
        overview_map,
        # overview_heatmap,
    ],
    style=OVERVIEW_LEFT_STYLE,
)

OVERVIEW_RIGHT_STYLE = {
    "position": "fixed",
    "margin-left": "44rem",
    # "margin-top": "1rem",
    "padding": "1rem",
    "width": "55rem",
    "background-color": "#f8f9fa",
}
overview_right = html.Div(
    children=[
        overview_histogram,
        overview_topN_table
    ],
    style=OVERVIEW_RIGHT_STYLE,
)

OVERVIEW_STYLE = {
    "position": "fixed",
    "margin-left": "10rem",
    "padding": "1rem",
}

overview = html.Div(
    children=[
        html.H2("Overview"),
        html.Hr(),
        overview_left,
        overview_right,
    ],
    style=OVERVIEW_STYLE,
)

# TODO: overview page:
#     - Geo map
#     - Heatmap
#     - Histogram
#     - Top-N table
#     - scalable for different devices/platforms
