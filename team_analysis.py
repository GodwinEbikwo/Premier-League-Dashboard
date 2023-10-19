import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import dash_loading_spinners as dls
from header import Header
from stat_card_img import StatCardImage
from stat_card import StatCard

matches_df = pd.read_csv("./data/matches_df.csv")
misc_df = pd.read_csv("./data/squad_misc_df.csv")
player_df = pd.read_csv("./data/player_df.csv")

player_df.drop_duplicates(inplace=True)


# Define the layout of the app
team_analysis_page_content = dbc.Container([
    Header(matches_df),
    html.Div(children=[
        html.Div(
            children=[
                StatCardImage("Yellow Cards", "yellow-cards-label", "div1",
                              "./assets/images/yellow-card.png"),
                StatCardImage("Red Cards", "red-cards-label", "div2",
                              "./assets/images/red-card.png"),
                StatCard("Fouls Committed", "fouls-committed-label", "div3"),
                StatCard("Own Goals Conceded", "own-goals-label", "div4"),

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


                StatCard("Penalty Kicks Won", "pkwon-label", "div6"),
                StatCard("Top Scorer", "top-scorer-label", "div7"),

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
                                    dcc.Graph(id="top-scorers-chart")
                                ),
                            ]
                        ),
                    ]
                ),
            ], className="grid"
        )
    ], className="grid-bento"),

], style={"padding": "2rem 1rem"})


@callback(
    Output("team-dropdown", "options"),
    Output("team-dropdown", "value"),
    Input("season-dropdown", "value")
)
def update_team_dropdown(selected_season):
    # Filter squad_misc_stats to get teams for the selected season
    teams_for_season = matches_df[matches_df["season"]
                                  == selected_season]["team"].unique()

    # Create dropdown options for the filtered teams
    team_options = [{'label': t, 'value': t} for t in teams_for_season]

    default_team_value = team_options[0]['value']

    return team_options, default_team_value


# Just new added code ----------------------------------------------------------
@callback(
    Output("team-goals-stats", "children"),
    Input("team-dropdown", "value"),
    Input("season-dropdown", "value")
)
def update_team_goals_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return []

    filtered_df = matches_df.loc[(matches_df["team"] == selected_team) & (
        matches_df["season"] == selected_season)]

    total_goals = filtered_df["gf"].sum()
    goals_against = filtered_df["ga"].sum()

    return dcc.Graph(
        figure=px.bar(
            x=["Goals Scored", "Goals Against"],
            y=[total_goals, goals_against],
            labels={"y": "Count", "x": ""}, text_auto=True,
        ).update_layout(
            xaxis_title="Round", yaxis_title="Goals",
            paper_bgcolor="rgb(255,255,255,255)",
            plot_bgcolor="rgb(255,255, 255,255)",
            title=f"Scored vs Conceded {selected_team} in {selected_season}",
        ),
    )


@callback(
    Output("pie-goal-stats", "children"),
    Output("timeline-chart", "children"),
    Input("team-dropdown", "value"),
    Input("season-dropdown", "value"),
)
def update_team_overall_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return {}, {}

    filtered_df = matches_df[(matches_df["team"] == selected_team) &
                             (matches_df["season"] == selected_season)].copy()

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
            plot_bgcolor="rgb(255,255,255,255)",
        )
    )

    return pie_goal_stats, line_gg


def calculate_team_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return 0, 0, 0, 0

    filtered_squad_df = misc_df[
        (misc_df["team"] == selected_team) &
        (misc_df["season"] == selected_season)
    ]

    print(filtered_squad_df.info())

    # Calculate yellow and red cards
    yellow_cards = filtered_squad_df["yellow_card"].sum()

    red_cards = filtered_squad_df["red_card"].sum()

    fouls_committed = filtered_squad_df["fouls_committed"].sum()
    own_goals = filtered_squad_df["own_goals"].sum()

    pkwon = filtered_squad_df["pkwon"].sum()

    return yellow_cards, red_cards, fouls_committed, own_goals, pkwon


@callback(
    [
        Output("yellow-cards-label", "children"),
        Output("red-cards-label", "children"),
        Output("fouls-committed-label", "children"),
        Output("own-goals-label", "children"),
        Output("pkwon-label", "children"),
    ],
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value"),
    ]
)
def update_team_stats(selected_team, selected_season):
    yellow_cards, red_cards, fls, own_goals, pkwon = calculate_team_stats(
        selected_team, selected_season)

    yellow_cards_label = f"{yellow_cards}"
    red_cards_label = f"{red_cards}"
    fouls_committed = f"{fls}"
    own_goals_label = f"{own_goals}"
    pkwon_label = f"{pkwon}"

    return yellow_cards_label, red_cards_label, fouls_committed, own_goals_label, pkwon_label


def calculate_team_top_scorer(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return "Select a team and season"

    # Filter dataframe
    team_df = player_df[(player_df["team"] == selected_team) &
                        (player_df["season"] == selected_season)]

    if team_df.empty:
        return f"No player data for {selected_team} in {selected_season}"

    # Remove unwanted rows
    filtered_df = team_df[~team_df['player'].isin(
        ['Opponent Total', 'Squad Total'])]

    # Ensure 'gls' column is numeric
    filtered_df['gls'] = pd.to_numeric(filtered_df['gls'], errors='coerce')

    # Get player with max goals
    top_scorer = filtered_df.loc[filtered_df['gls'].idxmax(), 'player']
    goals_scored = filtered_df['gls'].max()

    return top_scorer, goals_scored


@callback(
    Output("top-scorer-label", "children"),
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value")
    ]
)
def update_top_scorer(selected_team, selected_season):
    top_scorer, goals_scored = calculate_team_top_scorer(
        selected_team, selected_season)

    top_scorer_label = f"{top_scorer} with {goals_scored} goals"

    return top_scorer_label


def team_top_scorers(player_df, selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return "Select a team and season"

    # Ensure 'season' column is the appropriate type (string)
    # If your 'season' column is already an integer, comment out the line below
    # player_df['season'] = player_df['season'].astype(str)

    # Filter the player data for the selected team and season
    team_df = player_df[(player_df["team"] == selected_team) &
                        (player_df["season"].astype(str) == str(selected_season))]  # Convert season to string for comparison

    if team_df.empty:
        return f"No player data found for {selected_team} in {selected_season}"

    # Ensure 'gls' column is numeric
    team_df['gls'] = pd.to_numeric(team_df['gls'], errors='coerce')

    # Find the top 5 scorers
    top_scorers = team_df.nlargest(5, 'gls')[['player', 'gls']]

    return top_scorers


@callback(
    Output("top-scorers-chart", "figure"),
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value")
    ]
)
def update_top_scorers_chart(selected_team, selected_season):
    top_scorers = team_top_scorers(player_df, selected_team, selected_season)

    # If the returned value is a string, it means there was an error
    if isinstance(top_scorers, str):
        return dash.no_update

    fig = px.bar(top_scorers, x='player', y='gls',
                 title=f"Top Scorers for {selected_team} in {selected_season}")
    return fig
