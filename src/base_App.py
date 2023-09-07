import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import dash_loading_spinners as dls

df = pd.read_csv("preprocessed_match_data.csv")

squad_misc_stats = pd.read_csv("squad_misc_stats.csv")

# print(df.time)

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


# Create a summary card
def generate_summary_card(header, value, id):
    return dbc.Card([
        dbc.CardHeader(header),
        dcc.Loading(
            dbc.CardBody(value, id=id),
            type="default",
        ),
    ])


# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="team-dropdown",
                options=[{'label': t, 'value': t}
                         for t in df['team'].unique()],
                value=df['team'].iloc[0],
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
    dbc.Row([
        dbc.Col([
            html.Div(id="team-summary-cards", className="summary-cards"),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="team-overall-results-pie-chart",
                      className="pie-chart"),
        ]),
        dbc.Col([
            dcc.Graph(id="team-goals-bar-chart", className="bar-chart"),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="team-goals-line-chart", className="line-chart"),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="attendance-histogram", className="histogram"),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="venue-performance-bar-chart", className="bar-chart"),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="shot-efficiency-scatter", className="scatter"),
        ]),
    ]),
    html.Div(children=[
        html.Div(
            children=[
                html.Div(
                    id="team-goals-stats-container",
                    className="item item-2",
                    children=[
                        html.Div(
                            className="card-chart",
                            children=[
                                dcc.Loading(
                                    dls.Bounce(
                                        id="team-goals-stats",
                                        debounce=0
                                    ),
                                    type="default"
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    id="pie-goal-stats-container",
                    className="item item-3",
                    children=[
                        html.Div(
                            className="card-chart",
                            children=[
                                dcc.Loading(
                                    dls.Bounce(
                                        id="pie-goal-stats",
                                        debounce=0
                                    ),
                                    type="default"
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(
                    id="timeline-chart-container",
                    className="item item-1",
                    children=[
                        html.Div(
                            className="card-chart",
                            children=[
                                dcc.Loading(
                                    dls.Bounce(
                                        id="timeline-chart",
                                        debounce=0
                                    ),
                                    type="default"
                                )
                            ]
                        ),
                    ]
                ),
                html.Div(id="yellow-cards-label",
                         className="item item-4"),
                html.Div(id="red-cards-label", className="item item-5"),
                html.Div(id="fouls-committed-label", className="item item-6"),
                html.Div(id="penalty-kicks-won-label",
                         className="item item-7"),
            ], className="grid-row"
        )
    ], className="grid-bento"),

], style={"padding": "2rem 1rem"})


# Create the team summary cards
# Create the team summary cards
def create_summary_cards(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return []

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]

    print("Selected Team:", selected_team)
    print("Selected Season:", selected_season)
    print("Filtered DataFrame Size:", filtered_df.shape[0])

    if filtered_df.empty:
        return [generate_summary_card("No Data Available", "N/A", "no-data-card")]

    total_goals = filtered_df["gf"].sum()
    goals_against = filtered_df["ga"].sum()
    most_used_formation = filtered_df["formation"].value_counts().idxmax()
    free_kicks = filtered_df["fk"].sum()
    avg_possession = filtered_df["poss"].mean()
    median_attendance = filtered_df["attendance"].median()
    penalty_kicks = filtered_df["pk"].sum()
    expected_goals = filtered_df["xg"].sum()
    expected_goals_against = filtered_df["xga"].sum()
    matches_played = filtered_df.shape[0]

    cards = [
        generate_summary_card("Total Goals", total_goals, "total-goals"),
        generate_summary_card("Goals Against", goals_against, "goals-against"),
        generate_summary_card("Most Used Formation",
                              most_used_formation, "most-used-formation"),
        generate_summary_card("Free Kicks", free_kicks, "free-kicks"),
        generate_summary_card("Average Possession",
                              f"{avg_possession:.2f}%", "avg-possession"),
        generate_summary_card("Median Attendance",
                              median_attendance, "median-attendance"),
        generate_summary_card("Penalty Kicks", penalty_kicks, "penalty-kicks"),
        generate_summary_card("Expected Goals (xG)",
                              f"{expected_goals:.0f}", "expected-goals"),
        generate_summary_card("Expected Goals Against (xGA)",
                              f"{expected_goals_against:.0f}", "expected-goals-against"),
        generate_summary_card(
            "Matches Played", matches_played, "matches-played"),
    ]

    # Group the summary cards into sets of three
    summary_cards_sets = [cards[i:i+3] for i in range(0, len(cards), 3)]

    # Create a list of dbc.Row components, each containing a set of three summary cards
    summary_rows = [dbc.Row(
        [dbc.Col(card, className="col-4 mb-3 mt-3") for card in card_set],
        className="summary-row"
    ) for card_set in summary_cards_sets]

    return dcc.Loading(
        summary_rows,
        type="default"  # Choose a loading spinner type
    )


@app.callback(
    [Output("team-summary-cards", "children"),
     Output("team-goals-line-chart", "figure"),
     Output("team-overall-results-pie-chart", "figure")],  # Output for the pie chart
    [Input("team-dropdown", "value"),
     Input("season-dropdown", "value")]
)
def update_team_summary(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return [], {}, {}

    summary_cards = create_summary_cards(selected_team, selected_season)

    # Create a line chart for team's goals over rounds in the selected season
    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]
    filtered_df["round_numeric"] = filtered_df["round"].str.extract(
        r'(\d+)').astype(int)
    filtered_df = filtered_df.sort_values(by="round_numeric", ascending=True)
    filtered_df = filtered_df.drop(columns=["round_numeric"])

    # Create a pie chart for team's overall results
    overall_results = filtered_df["result"].value_counts()
    pie_chart = go.Figure(
        data=[go.Pie(labels=overall_results.index,
                     values=overall_results.values, hole=.3)]
    )
    pie_chart.update_layout(
        title=f"Overall Results for {selected_team} in {selected_season}",
    )

    line_chart = px.line(filtered_df, x="round", y="gf", markers=True,
                         title=f"Goals by Round for {selected_team} in {selected_season}")
    line_chart.update_layout(xaxis_title="Round", yaxis_title="Goals")

    return summary_cards, line_chart, pie_chart


@app.callback(
    Output("team-goals-bar-chart", "figure"),
    [Input("team-dropdown", "value"),
     Input("season-dropdown", "value")]
)
def update_goals_bar_chart(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return {}

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]

    goals_scored = filtered_df["gf"].sum()
    goals_conceded = filtered_df["ga"].sum()

    bar_chart = go.Figure(
        data=[
            go.Bar(x=["Goals Scored", "Goals Conceded"],
                   y=[goals_scored, goals_conceded])
        ],
        layout=go.Layout(
            title=f"Goals Scored vs Conceded for {selected_team} in {selected_season}")
    )

    return bar_chart


@app.callback(
    Output("attendance-histogram", "figure"),
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value")
    ]
)
def update_attendance_histogram(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return {}

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]
    attendance_data = filtered_df["attendance"]

    histogram_fig = go.Figure(
        data=[go.Histogram(x=attendance_data, nbinsx=20)],
        layout=go.Layout(
            title=f"Attendance Distribution for {selected_team} in {selected_season}",
            xaxis_title="Attendance",
            yaxis_title="Frequency"
        )
    )

    return histogram_fig


@app.callback(
    Output("venue-performance-bar-chart", "figure"),
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value")
    ]
)
def update_venue_performance_bar_chart(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return {}

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]

    venue_performance_fig = px.bar(
        filtered_df,
        x='venue',
        y='gf',
        color='venue',
        title='Performance at Different Venues',
        labels={'gf': 'Goals Scored'}
    )

    return venue_performance_fig


@app.callback(
    Output("shot-efficiency-scatter", "figure"),
    [Input("team-dropdown", "value"),
     Input("season-dropdown", "value")]
)
def update_shot_efficiency_scatter(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return {}

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]

    shot_efficiency_fig = px.scatter(
        filtered_df,
        x='sot',
        y='gf',
        title='Shot Efficiency Comparison',
        labels={'sot': 'Shots on Target', 'gf': 'Goals Scored'},
        color_discrete_sequence=['blue'],
        # Explicitly set the symbol to avoid the error
        symbol_sequence=['circle']
    )

    return shot_efficiency_fig


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
            title=f"Goals by Round for {selected_team} in {selected_season}",
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
            plot_bgcolor="rgb(255,255, 255,255)",)
    )

    return pie_goal_stats, line_gg,


def calculate_team_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return 0, 0

    filtered_squad_df = squad_misc_stats[
        (squad_misc_stats["team"] == selected_team) &
        (squad_misc_stats["season"] == selected_season)
    ]

    # Calculate yellow and red cards
    yellow_cards = filtered_squad_df["yellow_card"].sum()
    red_cards = filtered_squad_df["red_card"].sum()
    fouls_committed = filtered_squad_df["fouls_committed"].sum()
    pkwon = filtered_squad_df["pkwon"].sum()

    return yellow_cards, red_cards, fouls_committed, pkwon


@app.callback(
    [
        Output("yellow-cards-label", "children"),
        Output("red-cards-label", "children"),
        Output("fouls-committed-label", "children"),
        Output("penalty-kicks-won-label", "children"),
    ],
    [
        Input("team-dropdown", "value"),
        Input("season-dropdown", "value"),
    ]
)
def update_team_stats(selected_team, selected_season):
    yellow_cards, red_cards, fls, pkwon = calculate_team_stats(
        selected_team, selected_season)

    yellow_cards_label = f"Yellow Cards: {yellow_cards}"
    red_cards_label = f"Red Cards: {red_cards}"
    fouls_committed = f"Fouls Committed: {fls}"
    pkwon = f"Penalty Kicks won: {pkwon}"

    return yellow_cards_label, red_cards_label, fouls_committed, pkwon


if __name__ == "__main__":
    app.run_server(debug=True)
