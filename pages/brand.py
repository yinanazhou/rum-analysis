import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
import plotly.figure_factory as ff
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path="/brand", name="Brand", order=3)

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

####################### PAGE LAYOUT #############################

title = html.Div(
    children=[
        html.Br(),
        html.H2("Explore Top Rum Brands", className="fw-bold text-center"),
    ],
    className="mx-auto",
)

layout = html.Div(
    children=[
        title,
    ],
    className="mx-auto",
)
