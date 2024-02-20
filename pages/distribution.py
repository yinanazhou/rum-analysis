import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path="/distribution", name="Distribution", order=2)

####################### LOAD DATASET #############################
df = pd.read_csv("assets/merged_popularity.csv")
qc_df = df[df["Quebec"] == True]
columnDict = {
    "Popularity": "Popularity_scaled",
    "Number of Ratings": "nRatings",
    "Score": "Score",
    "Alcohol By Volumn": "ABV",
}
rum_type_options = sorted(list(df["Type"].unique()))
color_scale = px.colors.qualitative.Plotly


####################### FIGURES ###############################
def create_piecharts(ww, qc):
    fig = make_subplots(
        rows=2,
        cols=1,
        vertical_spacing=0.08,
        specs=[[{"type": "domain"}], [{"type": "domain"}]],
    )

    type_counts = ww.value_counts()
    qc_type_counts = qc.value_counts()
    fig.add_trace(
        go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            name="Worldwide",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Pie(
            labels=qc_type_counts.index,
            values=qc_type_counts.values,
            name="Quebec",
        ),
        row=2,
        col=1,
    )

    fig.update_traces(hole=0.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="Distribution of Rum Products by Type",
        title_font_size=14,
        title_y=0.95,
        annotations=[
            dict(text="Worldwide", x=0.5, y=0.2, showarrow=False),
            dict(text="Quebec", x=0.5, y=0.8, showarrow=False),
        ],
        legend_orientation="h",
        legend_y=0,
        # legend_x=0,
        # legend_xref="container",
        legend_yref="container",
        legend_itemwidth=30,
        # legend_entrywidth=40,
        # legend_entrywidthode
        margin_t=60,
        margin_b=0,
        margin_l=0,
        margin_r=0,
    )
    return fig


def create_distribution(feat_column, col, qc_col):
    dist_data = [col, qc_col]

    fig = ff.create_distplot(
        dist_data,
        group_labels=["Worldwide", "Quebec"],
        show_hist=False,
    )
    margin_x = 80
    margin_y = 40
    fig.update_layout(
        margin={
            "b": margin_y + 20,
            "l": margin_x,
            "t": margin_y,
            "r": margin_x,
        },
        xaxis_title=feat_column,
    )
    if columnDict[feat_column] == "ABV":
        fig.update_layout(xaxis=dict(tickformat=".0%"))
    elif columnDict[feat_column] == "ABV":
        fig.update_layout(yaxis=dict(tickformat=".0%"))
    return fig


####################### WIDGETS ################################

# Get color for checklist
colors = [
    color_scale[df["Type"].value_counts().index.tolist().index(t)]
    for t in rum_type_options
]
feat_dropdown = dcc.Dropdown(
    id="feat_column",
    options=list(columnDict.keys()),
    value="Popularity",
    clearable=False,
    className="pb-2",
)

feat_dropdown_container = html.Div(children=[feat_dropdown], className="col-3")

type_checklist = [
    {
        "label": html.Div(
            [rum_type_options[i]],
            style={
                "display": "inline",
                "color": colors[i],
            },
            id={"type": "label-" + rum_type_options[i]},
            className="p-1 me-3 checklist-label",
        ),
        "value": rum_type_options[i],
    }
    for i in range(len(rum_type_options))
]

type_option = dcc.Checklist(
    type_checklist,
    value=rum_type_options,
    labelStyle={"display": "inline-flex"},
    inline=True,
    className="justify-content-center d-flex ps-2 mb-2",
    style={
        "backgroundColor": "white",
        "borderRadius": "10px",
    },
    id="type-checklist",
)

filter_row = html.Div(
    children=[type_option],
    className="row align-items-center",
    id="checklist-row",
)
filter_container = html.Div(children=[filter_row], className="container my-auto")
filter_panel = html.Div(children=[filter_container], className="col-8 my-auto")

widget_row = html.Div(
    children=[
        feat_dropdown_container,
        filter_panel,
    ],
    className="row justify-content-between",
)

widget = html.Div(
    children=[widget_row],
    className="container mx-auto",
)
####################### LEFT LAYOUT #############################

pie_plot = dcc.Graph(
    figure=create_piecharts(df["Type"], qc_df["Type"]), className="col-3 px-2", id="pie"
)

####################### RIGHT LAYOUT #############################


dist_plot = dcc.Graph(id="distogram", style={"height": "70vh"})

right_pane = html.Div(
    children=[widget_row, dist_plot],
    className="col-9 mx-auto",
)

####################### PAGE LAYOUT #############################
title = html.Div(
    children=[
        html.Br(),
        html.H2(
            "Explore Distribution of Feature Values", className="fw-bold text-center"
        ),
    ],
    className="mx-auto",
)

main_row = html.Div(
    children=[pie_plot, right_pane],
    className="row mx-auto",
)

main_container = html.Div(
    children=[main_row],
    className="container mx-auto",
)

mainPanel = html.Div(
    children=[
        html.Br(),
        main_container,
    ],
    className="col-12 mx-auto",
)

layout = html.Div(
    children=[
        title,
        mainPanel,
    ],
    className="mx-auto",
)


####################### CALLBACKS ################################


@callback(
    Output("distogram", "figure"),
    [
        Input("feat_column", "value"),
        Input("type-checklist", "value"),
    ],
)
def update_histogram(feat_column, selected_types):
    filtered_df = df[df["Type"].isin(selected_types)]
    qc_filtered_df = qc_df[qc_df["Type"].isin(selected_types)]
    return create_distribution(
        feat_column,
        filtered_df[columnDict[feat_column]].dropna(),
        qc_filtered_df[columnDict[feat_column]].dropna(),
    )
