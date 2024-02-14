import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/relationship", name="Relationship", order=3)

####################### DATASET #############################
df = pd.read_csv("assets/merged_popularity.csv")
columnDict = {
    "Popularity": "Popularity_scaled",
    "Number of Ratings": "nRatings",
    "Score": "Score",
    "Unit Price (CAD)": "Price_unit",
    "Type": "Rum Type",
    "Alcohol By Volumn": "ABV",
}
rum_type_options = sorted(list(df["Type"].unique()))

####################### WIDGETS #############################
x_axis = dcc.Dropdown(
    id="x_axis",
    options=list(columnDict.keys()),
    value="Unit Price (CAD)",
    clearable=False,
)
y_axis = dcc.Dropdown(
    id="y_axis", options=list(columnDict.keys()), value="Popularity", clearable=False
)

####################### PAGE LAYOUT #############################
title = html.Div(
    children=[
        html.Br(),
        html.H2(
            "Explore Relationship between Features", className="fw-bold text-center"
        ),
    ],
    className="mx-auto",
)

mainPanel = html.Div(
    children=[
        "X-Axis",
        x_axis,
        "Y-Axis",
        y_axis,
        html.Br(),
        dcc.Graph(id="scatter"),
    ],
    className="col-9 mx-auto",
)

layout = html.Div(
    children=[
        title,
        mainPanel,
    ],
    className="mx-auto",
)

color_scale = px.colors.qualitative.Set1


####################### CALLBACKS ###############################
@callback(
    Output("scatter", "figure"),
    [
        Input("x_axis", "value"),
        Input("y_axis", "value"),
    ],
)
def update_scatter_chart(x_axis, y_axis):
    log_x = False
    log_y = False
    if x_axis == "Unit Price (CAD)":
        log_x = True
    elif y_axis == "Unit Price (CAD)":
        log_y = True
    fig = px.scatter(
        data_frame=df.sort_values(by="Type"),
        x=columnDict[x_axis],
        y=columnDict[y_axis],
        color="Type",
        height=500,
        labels={
            columnDict[x_axis]: x_axis,
            columnDict[y_axis]: y_axis,
            "Type": columnDict["Type"],
        },
        log_y=log_y,
        log_x=log_x,
    )
    fig.update_traces(marker={"size": 5, "opacity": 0.85})
    fig.update_layout(margin_autoexpand=True)
    fig.update_layout(legend={"entrywidth": 100})
    if columnDict[x_axis] == "ABV":
        fig.update_layout(xaxis=dict(tickformat=".0%"))
    elif columnDict[y_axis] == "ABV":
        fig.update_layout(yaxis=dict(tickformat=".0%"))
    return fig
