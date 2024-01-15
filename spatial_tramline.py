from dash import html, dcc, Input, Output
import plotly.express as px

from data import data

BARPLOT_SPATIAL_TRAMLINE_STYLE = {
    "width": "auto",
    "padding": "1rem",
    "background-color": "#f8f9fa",
}
barplot_spatial_tramline_figure = px.bar(
    data_frame=data.groupby("continent").count(),
    x=data.groupby("continent").count().index,
    y="country",
    title="The distribution of speed",
    width=1500,
)
barplot_spatial_tramline = html.Div(
    children=[
        dcc.Graph(
            figure=barplot_spatial_tramline_figure,
        )
    ],
    style=BARPLOT_SPATIAL_TRAMLINE_STYLE,
)

SPATIAL_TRAMLINE_STYLE = {
    "position": "fixed",
    "margin-left": "10rem",
    "padding": "1rem",
}
spatial_tramline_layout = html.Div(
    children=[
        html.H2("Overview"),
        html.Hr(),
        barplot_spatial_tramline,
        dcc.Dropdown(
            options=data.groupby("continent").count().index,
            multi=True,
            style={
                "width": "40rem",
                # "padding": "0.5rem",
                # "background-color": "#f8f9fa",
            }
        )
    ],
    style=SPATIAL_TRAMLINE_STYLE,
)