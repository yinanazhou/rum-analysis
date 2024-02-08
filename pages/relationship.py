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


####################### SCATTER CHART #############################
def create_scatter_chart(x_axis, y_axis):
    log_x = False
    log_y = False
    if x_axis == "Unit Price (CAD)":
        log_x = True
    elif y_axis == "Unit Price (CAD)":
        log_y = True
    fig = px.scatter(
        data_frame=df,
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
    if columnDict[x_axis] == "ABV":
        fig.update_layout(xaxis=dict(tickformat=".0%"))
    elif columnDict[y_axis] == "ABV":
        fig.update_layout(yaxis=dict(tickformat=".0%"))
    return fig


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
layout = html.Div(
    children=[
        html.Br(),
        html.H2(
            "Explore Relationship between Features", className="fw-bold text-center"
        ),
        "X-Axis",
        x_axis,
        "Y-Axis",
        y_axis,
        html.Br(),
        dcc.Graph(id="scatter"),
    ]
)


####################### CALLBACKS ###############################
@callback(
    Output("scatter", "figure"),
    [
        Input("x_axis", "value"),
        Input("y_axis", "value"),
    ],
)
def update_scatter_chart(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)
