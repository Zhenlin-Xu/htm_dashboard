from dash import html, dcc, dash_table
import plotly.express as px

from data import data

ROUNDRECTANGLE_STYLE = {
    "width": "8rem",
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
                html.H3(f"{len(data['country'].unique())}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE
        ),
        html.Div(
            children=[
                html.P("Straight overspeeding"),
                html.H3(f"{len(data['continent'].unique())}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE
        ),
        html.Div(
            children=[
                html.P("Turning overspeeding"),
                html.H3(f"{len(data['year'].unique())}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE,
        ),
        html.Div(
            children=[
                html.P("Turning overspeeding"),
                html.H3(f"{len(data['iso_num'].unique())}"),
                html.P("in 2023")
            ],
            style=ROUNDRECTANGLE_STYLE,
        ),
    ],
)

OVERVIEW_MAP_STYLE = {
    "position": "fixed",
    "width": "80rem",
}

overview_map_figure = px.scatter_geo(
    data_frame=data.query("year == 2027"),
    locations="iso_alpha",
    size="pop",
    width=600,
    height=400,
    title="The spatial distribution of the switch",
)
overview_map = html.Div(
    children=[
        dcc.Graph(
            figure=overview_map_figure
        ),
    ],
    style={"margin-top": "1rem"}
)

overview_heatmap_figure = px.imshow(
    img=[
        [1, 20, 30],
        [20, 1, 60],
        [30, 60, 1]
    ],
    title="The temporal distribution of overspeeding",
    width=600,
    height=400,
)
overview_heatmap = html.Div(
    children=[
        dcc.Graph(
            figure=overview_heatmap_figure
        ),
    ],
    style={"margin-top": "1rem"}
)

overview_histogram_figure = px.histogram(
    data_frame=data.groupby("continent").count(),
    x=data.groupby("continent").count().index,
    y="country",
    title="The distribution of speed",
)
overview_histogram = html.Div(
    children=[
        dcc.Graph(
            figure=overview_histogram_figure
        ),
    ],
    style={"margin-top": "1rem"}
)

overview_topN_table = html.Div(
    children=[
        dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[{'id': c, 'name': c} for c in data.columns],
            page_size=10,
        )
    ],
    style={"margin-top": "2rem"}
)

OVERVIEW_LEFT_STYLE = {
    "position": "fixed",
    "padding": "1rem",
    "background-color": "#f8f9fa",
}
overview_left = html.Div(
    children=[
        round_rectangles,
        overview_map,
        overview_heatmap,
    ],
    style=OVERVIEW_LEFT_STYLE,
)

OVERVIEW_RIGHT_STYLE = {
    "position": "fixed",
    "margin-left": "40rem",
    # "margin-top": "1rem",
    "padding": "1rem",
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
