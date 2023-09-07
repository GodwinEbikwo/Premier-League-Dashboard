import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import dash_loading_spinners as dls


df = pd.read_csv("matches_df.csv")
squad_misc_stats = pd.read_csv("squad_misc_stats.csv")
player_df = pd.read_csv("clean_player_data.csv")


# Define a dictionary of team name replacements
team_name_replacements = {
    'Wolves': 'Wolverhampton Wanderers',
    'Manchester Utd': 'Manchester United',
    'Newcastle Utd': 'Newcastle United',
    'West Ham': 'West Ham United',
    'Tottenham': 'Tottenham Hotspur',
    'Nott\'ham Forest': 'Nottingham Forest',
    'West Brom': 'West Bromwich Albion',
    'Brighton': 'Brighton and Hove Albion',
    'Sheffield Utd': 'Sheffield United',
    'Huddersfield': 'Huddersfield Town',
}

# Apply the replacements to the 'team' column
squad_misc_stats['team'] = squad_misc_stats['team'].replace(
    team_name_replacements)


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
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                placeholder="Please select a team",
                id="team-dropdown",
                options=[],
                value='',
                multi=False),
        ]),
        dbc.Col([
            dcc.Dropdown(
                id="season-dropdown",
                options=[{'label': s, 'value': s}
                         for s in df['season'].unique()],
                value=df['season'].iloc[0],
                multi=False),
        ]),
    ]),
    html.Div(children=[
        html.Div(
            children=[
                html.Div(className="grid__card div1", children=[
                    html.Div(className="card-body", children=[
                        html.Div(className="d-flex justify-content-between",
                                 children=[
                                     html.Div(className="card-info w-100",
                                              children=[html.Small(
                                                  className="card-text", children=["Yellow Cards"]),
                                                  dls.Triangle(
                                                  html.H2(
                                                      className="mb-2 mt-2 card-title mb-2",
                                                      id="yellow-cards-label",
                                                      style={"font-size": "3vw"})),
                                                  html.Small(className="card-text",
                                                             children=[
                                                                 "In the 38 games"]
                                                             )
                                              ], style={"text-align": "center"}),

                                     html.Div(
                                         className="card-icon d-flex align-items-center w-50",
                                         children=[
                                             html.Img(
                                                 className="img-fluid bx-lg",
                                                 src="./assets/images/yellow-card.png", style={"width": "4rem"})
                                         ]
                                     )
                                 ])

                    ])
                ]),
                html.Div(className="grid__card div2", children=[
                    html.Div(className="card-body", children=[
                        html.Div(className="d-flex justify-content-between", children=[
                            html.Div(className="card-info w-100",
                                     children=[
                                         html.Small(
                                             className="card-text", children=["Red Cards"]),
                                         dls.Triangle(
                                             html.H2(
                                                 className="mb-2 mt-2 card-title mb-2",
                                                 id="red-cards-label",
                                                 style={"font-size": "3vw"})),
                                         html.Small(
                                             className="card-text",
                                             children=["In the 38 games"]
                                         )
                                     ], style={"text-align": "center"}),
                            html.Div(
                                className="card-icon d-flex align-items-center w-50", children=[
                                    html.Img(
                                        className="img-fluid bx-lg",
                                        src="./assets/images/red-card.png", style={"width": "4rem"})
                                ]
                            )
                        ])

                    ])
                ]),
                html.Div(className="grid__card div3", children=[
                    html.Div(className="card-body", children=[
                        html.Div(className="d-flex justify-content-between", children=[
                            html.Div(className="card-info w-100",
                                     children=[html.Small(className="card-text", children=["Own Goals Conceded"]),
                                               dls.Triangle(
                                         html.H2(className="mb-2 mt-2 card-title mb-2",
                                                 id="own-goals-label",
                                                 style={"font-size": "3vw"})),
                                               html.Small(
                                                   className="card-text",
                                         children=[
                                             "In the 38 games"]
                                     )
                                     ], style={"text-align": "center"}),
                        ])
                    ])
                ]),

                html.Div(className="grid__card div4", children=[
                    html.Div(className="card-body", children=[
                        html.Div(className="d-flex justify-content-between", children=[
                            html.Div(className="card-info w-100",
                                     children=[html.Small(className="card-text", children=["Fouls Committed"]),
                                               dls.Triangle(
                                         html.H2(className="mb-2 mt-2 card-title mb-2",
                                                 id="fouls-committed-label",
                                                 style={"font-size": "3vw"})),
                                               html.Small(
                                         className="card-text",
                                         children=[
                                             "In the 38 games"]
                                     )
                                     ], style={"text-align": "center"}),
                        ])
                    ])
                ]),
                html.Div(
                    id="timeline-chart-container",
                    className="grid__card div5",
                    children=[
                        html.Div(
                            children=[
                                dls.Triangle(
                                    id="timeline-chart",
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="grid__card div6",
                    children=[
                        "In the 38 games"
                    ]
                ),

                html.Div(className="grid__card div7", children=[
                    html.Div(className="card-body", children=[
                        html.Div(className="d-flex", children=[
                            html.Div(className="card-info w-100",
                                     children=[html.Small(className="card-text", children=["Top Scorer"]),
                                               dls.Triangle(
                                         html.H2(className="mb-2 mt-2 card-title mb-2",
                                                 id="top-scorer-label",
                                                 style={"font-size": "3vw"})),

                                               html.Small(
                                         className="card-text",
                                         children=[
                                             "In the 38 games"]
                                     )
                                     ], style={"text-align": "center"}),
                        ])
                    ])
                ]),
                html.Div(
                    className="grid__card div8",
                    children=[
                        html.Div(
                            children=[
                                dls.Triangle(
                                    id="team-goals-stats",
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="grid__card div9",
                    children=[
                        html.Div(
                            children=[
                                dls.Triangle(
                                    id="pie-goal-stats",
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="grid__card div10",
                    children=[
                        html.Div(
                            children=[
                                dls.Triangle(
                                    id="attendance-trend-chart",
                                ),
                            ]
                        ),
                    ]
                ),
            ], className="grid"
        )
    ], className="grid-bento"),

], style={"padding": "2rem 1rem"})


@app.callback(
    Output("team-dropdown", "options"),
    Output("team-dropdown", "value"),  # Add this line to set the default value
    Input("season-dropdown", "value")
)
def update_team_dropdown(selected_season):
    # Filter squad_misc_stats to get teams for the selected season
    teams_for_season = df[df["season"] == selected_season]["team"].unique()

    # Create dropdown options for the filtered teams
    team_options = [{'label': t, 'value': t} for t in teams_for_season]

    # Set the default value to the first team in the options
    default_team_value = team_options[0]['value']

    # Return both options and default value
    return team_options, default_team_value


# Just new added code ----------------------------------------------------------
@app.callback(
    Output("team-goals-stats", "children"),
    Input("team-dropdown", "value"),
    Input("season-dropdown", "value")
)
def update_team_goals_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return []

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]

    total_goals = filtered_df["gf"].sum()
    goals_against = filtered_df["ga"].sum()

    return dcc.Graph(
        figure=px.bar(
            x=["Goals Scored", "Goals Against"],
            y=[total_goals, goals_against],
            labels={"y": "Count", "x": ""}, text_auto=True,
            # Specify the color mapping
            # color=["Goals Scored", "Goals Against"],
            # color_discrete_map={"Goals Scored": "#52b788",
            #                     "Goals Against": "#ef233c"},
        ).update_layout(
            xaxis_title="Round", yaxis_title="Goals",
            paper_bgcolor="rgb(255,255,255,255)",
            plot_bgcolor="rgb(255,255, 255,255)",
            title=f"Goals Scored & Conceded by {selected_team} in {selected_season}",
        ),
    )


@app.callback(

    [
        Output("pie-goal-stats", "children"),
        Output("timeline-chart", "children"),
    ],

    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value")
    ]
)
def update_team_overall_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return {}

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]

    filtered_df["round_numeric"] = filtered_df["round"].str.extract(
        r'(\d+)').astype(int)
    filtered_df = filtered_df.sort_values(by="round_numeric", ascending=True)
    filtered_df = filtered_df.drop(columns=["round_numeric"])

    overall_results = filtered_df["result"].value_counts()
    pie_goal_stats = dcc.Graph(
        figure=go.Figure(
            data=[go.Pie(labels=overall_results.index,
                         values=overall_results.values, hole=.3)]
        ).update_layout(
            title=f"Overall Results for {selected_team} in {selected_season}",
        )
    )

    line_gg = dcc.Graph(
        figure=px.line(
            filtered_df, x="round", y="gf", markers=True,
        ).update_layout(
            title=f"Goals by Round for {selected_team} in {selected_season}",
            xaxis_title="Round", yaxis_title="Goals",
            paper_bgcolor="rgb(255,255,255,255)",
            plot_bgcolor="rgb(255,255,255,255)",)
    )

    return pie_goal_stats, line_gg,


def calculate_team_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return 0, 0, 0, 0

    filtered_squad_df = squad_misc_stats[
        (squad_misc_stats["team"] == selected_team) &
        (squad_misc_stats["season"] == selected_season)
    ]

    # Calculate yellow and red cards
    yellow_cards = filtered_squad_df["yellow_card"].sum()
    red_cards = filtered_squad_df["red_card"].sum()
    fouls_committed = filtered_squad_df["fouls_committed"].sum()
    own_goals = filtered_squad_df["own_goals"].sum()

    return yellow_cards, red_cards, fouls_committed, own_goals,


@app.callback(
    [
        Output("yellow-cards-label", "children"),
        Output("red-cards-label", "children"),
        Output("own-goals-label", "children"),
        Output("fouls-committed-label", "children"),
    ],
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value"),
    ]
)
def update_team_stats(selected_team, selected_season):
    yellow_cards, red_cards, fls, own_goals,  = calculate_team_stats(
        selected_team, selected_season)

    yellow_cards_label = f"{yellow_cards}"
    red_cards_label = f"{red_cards}"
    fouls_committed = f"{fls}"
    own_goals_label = f"{own_goals}"

    return yellow_cards_label, red_cards_label, fouls_committed,  own_goals_label,


@app.callback(
    [Output("attendance-trend-chart", "children")],
    [Input("team-dropdown", "value"), ]
)
def update_attendance_trend_chart(selected_team):
    if selected_team is None:
        return []

    # Filter the DataFrame for the selected team
    filtered_df = df[df["team"] == selected_team]

    # Create a line chart for attendance trend
    fig = px.line(
        filtered_df, x="season", y="attendance",
        title=f"Attendance Trend for {selected_team}",
        labels={"season": "Season", "attendance": "Attendance"},
    )

    fig.update_layout(
        paper_bgcolor="rgb(255, 255, 255, 255)",
        plot_bgcolor="rgb(255, 255, 255, 255)",
    )

    return [dcc.Graph(figure=fig)]


def calculate_team_scorers(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return "Select a team and season"

    # Filter the player data for the selected team and season
    team_season_data = player_df[(player_df["team"] == selected_team) &
                                 (player_df["season"] == selected_season)]

    if team_season_data.empty:
        return f"No top scorer found for {selected_team} in {selected_season}"

    filtered_data = team_season_data[
        ~team_season_data['player'].isin(['Opponent Total', 'Squad Total'])
    ]

    player_goals_sum = filtered_data.groupby('player')['gls'].sum()

    top_scorer = player_goals_sum.idxmax()
    goals_scored = player_goals_sum.max()

    return top_scorer, goals_scored


@app.callback(
    Output("top-scorer-label", "children"),
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value")
    ]
)
def update_top_scorer(selected_team, selected_season):
    top_scorer, goals_scored = calculate_team_scorers(
        selected_team, selected_season)

    top_scorer_label = f"{top_scorer} with {goals_scored} goals"

    return top_scorer_label


if __name__ == "__main__":
    app.run_server(debug=True)
