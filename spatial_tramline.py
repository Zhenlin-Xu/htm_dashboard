from dash import html, dcc, Input, Output
import plotly.express as px

from data import *

BARPLOT_SPATIAL_TRAMLINE_STYLE = {
    "width": "fit-content",
    "height": "20rem",
    # "padding": "1rem",
    "background-color": "#f8f9fa",
}
barplot_spatial_tramline_figure = px.bar(
    data_frame=number_overspeed_records_per_line,
    x=number_overspeed_records_per_line.index,
    y="switch_number",
    color="direction",
    barmode="group",
    # title="The distribution of speed",
    labels={
        "index": "Tram line",
        "switch_number": "Count",
    },
    height=300,
)
barplot_spatial_tramline_figure.update_layout(
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99),
    margin=dict(l=10, r=0, b=0, t=25),
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 0,
        dtick = 1,
    )
)
barplot_spatial_tramline = html.Div(
    children=[
        dcc.Graph(
            figure=barplot_spatial_tramline_figure,
        )
    ],
    style=BARPLOT_SPATIAL_TRAMLINE_STYLE,
)

BARPLOT_SPATIAL_SPEED_TRAMLINE_STYLE = {
    "width": "fit-content",
    "height": "20rem",
    # "padding": "1rem",
    "background-color": "#f8f9fa",
}
barplot_spatial_speed_tramline_figure = px.histogram(
    data_frame=n_os_per_speed_per_line[
        n_os_per_speed_per_line["line"].isin([1,])],
    x="speed",
    y="vehicle",
    color="direction",
    log_y=True,
    barmode="group",
    # marginal="box",
    # orientation='v',
    nbins=len(n_os_per_speed_per_line["speed"].unique()),
    height=300,
)
barplot_spatial_speed_tramline_figure.update_layout(
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
    margin=dict(l=10, r=0, b=0, t=25),
    xaxis=dict(tickmode='linear', tick0=SPEED_LIMIT, dtick=1)
)
barplot_spatial_speed_tramline = html.Div(
    children=[
        dcc.Graph(
            figure=barplot_spatial_speed_tramline_figure,
        )
    ],
    style=BARPLOT_SPATIAL_SPEED_TRAMLINE_STYLE,
)

CDF_STYLE = {

}
cdf_speed_tramline_figure = px.ecdf(
    data_frame=n_os_per_speed_per_line[
        n_os_per_speed_per_line["line"].isin([1,])
    ],
    x="speed",
    color="direction",
)
cdf_speed_tramline = html.Div(
    children=[
        dcc.Graph(
            figure=cdf_speed_tramline_figure,
        )
    ],
    style=CDF_STYLE
)

SPATIAL_TRAMLINE_STYLE = {
    "position": "fixed",
    "width": "fit-content",
    "margin-left": "10rem",
    "padding": "1rem",
}
spatial_tramline_layout = html.Div(
    children=[
        html.H2("Spatial analysis | Tramline"),
        html.Hr(),
        barplot_spatial_tramline,
        dcc.Dropdown(
            options=n_os_per_speed_per_line["line"].unique(),
            multi=True,
            style={
                "width": "40rem",
                # "padding": "0.5rem",
                # "background-color": "#f8f9fa",
            }
        ),
        barplot_spatial_speed_tramline,
        cdf_speed_tramline,
    ],
    style=SPATIAL_TRAMLINE_STYLE,
)