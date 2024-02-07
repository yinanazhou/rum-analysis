from dash import Dash, html, dcc
import dash

external_css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css",
]

app = Dash(
    __name__, pages_folder="pages", use_pages=True, external_stylesheets=external_css
)

img_tag = html.I(className="bi bi-droplet-half")
brand_link = dcc.Link([img_tag, "  RumRatings "], href="/", className="navbar-brand")
pages_links = [
    dcc.Link(page["name"], href=page["relative_path"], className="nav-link")
    for page in dash.page_registry.values()
    if not page["name"] == "index"  # skip index page as it is linked to brand
]
github_link = dcc.Link(
    html.I(className="bi bi-github"),
    href="https://github.com/yinanazhou/rum-analysis",
    className="nav-item",
    style={"color": "white", "font-size": "25px"},
)

app.layout = html.Div(
    [
        ### Navbar
        html.Nav(
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                brand_link,
                            ]
                            + pages_links,
                            className="navbar-nav",
                        ),
                        github_link,
                    ],
                    className="container-fluid",
                ),
            ],
            className="navbar navbar-expand-lg bg-dark",
            **{"data-bs-theme": "dark"}
        ),
        #### Main Page
        html.Div(
            [
                dash.page_container,
            ],
            className="col-8 mx-auto",
        ),
    ],
    style={"height": "100vh", "background-color": "#e3f2fd"},
)

if __name__ == "__main__":
    app.run(debug=True)
