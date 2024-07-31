import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path="/type", name="Type", order=3)

####################### LOAD DATASET #############################
df = pd.read_csv("assets/merged_popularity.csv")

avg_popularity = df.groupby("Type")["Popularity_scaled"].mean().reset_index().round(2)
avg_popularity_quebec = (
    df[df["Quebec"] == True]
    .groupby("Type")["Popularity_scaled"]
    .mean()
    .reset_index()
    .round(2)
)
type_counts = df.groupby("Type").size().reset_index(name="Count")
type_counts_quebec = (
    df[df["Quebec"] == True].groupby("Type").size().reset_index(name="Count_Quebec")
)
stats_df = (
    avg_popularity.merge(avg_popularity_quebec, on="Type", suffixes=("", "_Quebec"))
    .merge(type_counts, on="Type")
    .merge(type_counts_quebec, on="Type")
).sort_values(by="Count", ascending=False)

rum_type_options = sorted(list(df["Type"].unique()))
color_scale = px.colors.qualitative.Plotly
colors = [color_scale[stats_df["Type"].tolist().index(t)] for t in rum_type_options]


####################### FIGURES ###############################
def create_count_plot(types, count, count_qc):
    fig = go.Figure(
        data=[
            go.Bar(x=types, y=count, name="Worldwide", text=count),
            go.Bar(x=types, y=count_qc, name="Quebec", text=count_qc),
        ],
        layout=dict(
            barcornerradius=15,
            yaxis=dict(type="log"),
            xaxis_title="Type", 
            yaxis_title="Count"
        ),
    )
    return fig


def create_pop_plot(types, pop, pop_qc):
    fig = go.Figure(
        data=[
            go.Bar(x=types, y=pop, name="Worldwide", text=pop),
            go.Bar(x=types, y=pop_qc, name="Quebec", text=pop_qc),
        ],
        layout=dict(
            barcornerradius=15,
            xaxis_title="Type", 
            yaxis_title="Popularity"
        ),
    )
    return fig


####################### LEFT LAYOUT #############################
count_plot = dcc.Graph(
    figure=create_count_plot(
        stats_df["Type"],
        stats_df["Count"],
        stats_df["Count_Quebec"],
    ),
    className="col-6 px-2",
    id="count-bar",
)


####################### RIGHT LAYOUT #############################
pop_plot = dcc.Graph(
    figure=create_pop_plot(
        stats_df["Type"],
        stats_df["Popularity_scaled"],
        stats_df["Popularity_scaled_Quebec"],
    ),
    className="col-6 px-2",
    id="pop-bar",
)

####################### PAGE LAYOUT #############################

title = html.Div(
    children=[
        html.Br(),
        html.H2("Explore Top Rum Brands", className="fw-bold text-center"),
    ],
    className="mx-auto",
)

main_row = html.Div(
    children=[count_plot, pop_plot],
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
