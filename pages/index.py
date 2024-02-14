import dash
from dash import html

dash.register_page(__name__, path="/", name="index", title="Rum Demo", order=0)

####################### PAGE LAYOUT #############################
layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Br(),
                html.P(
                    "Rum Ratings Dashboard Demo",
                    className="text-dark text-center fw-bold fs-1",
                ),
                html.P(
                    "🥂",
                    className="text-dark text-center fw-bold fs-1",
                ),
            ],
            className="col-6 mx-auto",
        ),
        html.Div(
            children=[
                html.H2("Rum Dataset Overview"),
                "This dataset contains the rum information available at rumRatings.com, and the price information for the rum products available in Quebec from saq.ca.",
                html.Br(),
            ],
            className="col-6 mx-auto",
        ),
        html.Div(
            children=[
                html.Br(),
                html.H2("Data Variables"),
                "Number of Instances: 4,592",
                html.Br(),
                html.Br(),
                html.B("- Company"),
                html.Br(),
                html.B("- Name"),
                html.Br(),
                html.B("- Country"),
                html.Br(),
                html.B("- Type"),
                html.Br(),
                html.B("- Score"),
                html.Br(),
                html.B("- Number of Ratings"),
                html.Br(),
                html.B("- Popularity"),
            ],
            className="col-6 mx-auto",
        ),
    ],
    className="p-4 m-2",
)
