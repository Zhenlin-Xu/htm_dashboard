from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_leaflet as dl

from data_process.data import *

# top-left corner
round_rectangles = html.Div(
    children=[
        html.Div(
            children=[
                html.P("Overall overspeeding"),
                html.P(f"{len(overspeed)}", className="round-rectangle-foreground-number"),
                html.P("in 2023")
            ],
            className="round-rectangle-foreground"
        ),
        html.Div(
            children=[
                html.P("Straight overspeeding"),
                html.P(f"{len(straight_overspeed)}", className="round-rectangle-foreground-number"),
                html.P("in 2023")
            ],
            className="round-rectangle-foreground"
        ),
        html.Div(
            children=[
                html.P("Turning overspeeding"),
                html.P(f"{len(turning_overspeed)}", className="round-rectangle-foreground-number"),
                html.P("in 2023")
            ],
            className="round-rectangle-foreground"
        ),
        html.Div(
            children=[
                html.P("Percentage of overspeeding"),
                html.P(f"{len(overspeed)/len(speed):.2f}", className="round-rectangle-foreground-number"),
                html.P("in 2023")
            ],
            className="round-rectangle-foreground"
        ),
    ],
    className="round-rectangle-background"
)

# middle-left: map
# https://www.dash-leaflet.com
OVERVIEW_MAP_STYLE = {
    "position": "fixed",
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
    style={"height": "70vh", "width": "25vw"}
)
overview_map = dbc.Container(
    children=overview_map_figure,
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
    #     "margin-top": "1rem",
        "width": "35rem",
        "height": "30rem",
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
    style={
        # "margin-top": "10rem",
        "width": "30rem",
    }
)

overview_left = dbc.Container(
    children=[
        round_rectangles,
        overview_map,
        # overview_heatmap,
    ],
    style={
        "display": "inline-block",
        "width": "26.5vw",
        "margin-left": "1rem",
    }
)

OVERVIEW_RIGHT_STYLE = {
    "margin-top": "-70rem",
    "margin-left": "45rem",
    # "padding": "1rem",
    "width": "30rem",
    "height": "40rem",
    # "display": "inline-block",
}
overview_right = dbc.Container(
    children=[
        overview_histogram,
        overview_topN_table
    ],
    style=OVERVIEW_RIGHT_STYLE,
)

overview_layout = dbc.Container(
    children=[
        html.H2(html.Strong("Overview"), className="content-header"),
        html.Hr(),
        overview_left,
        overview_right,
    ],
    className="content-global-style"
)

# TODO: overview page:
#     - Geo map
#     - Heatmap
#     - Histogram
#     - Top-N table
#     - scalable for different devices/platforms
