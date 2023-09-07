import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from team_analysis import team_analysis_page_content
from player_analysis import head_to_head_page_content

# layout styling
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "2rem 1rem",
    "background-color": "#fff",
}

CONTENT_STYLE = {
    "margin-left": "13rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Teams", href="/page-1", active="exact"),
                dbc.NavLink("Players", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# data
matches_df = pd.read_csv("matches_df.csv")
misc_df = pd.read_csv("squad_misc_stats.csv")
player_df = pd.read_csv("clean_player_data.csv")

data_store = html.Div([dcc.Store(id="teams-df", data=matches_df.to_json()),
                       dcc.Store(id="squad-misc-df", data=misc_df.to_json()),
                       dcc.Store(id="player-df", data=player_df.to_json())])

# style sheet
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=IBM+Plex+Sans:wght@400;500&display=swap"
        ),
        "rel": "stylesheet",
    },
    dbc.themes.BOOTSTRAP,
]

# Initialize the Dash app
app = dash.Dash(__name__, title="Premier League Dashboard",
                external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div(children=[
    dcc.Location(id="url"),
    data_store,
    html.Aside(className="", children=[sidebar]), content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return team_analysis_page_content
    elif pathname == "/page-2":
        return head_to_head_page_content
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
