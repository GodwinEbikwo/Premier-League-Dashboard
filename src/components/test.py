import plotly.express as px
import pandas as pd
from dash import html, dcc
import utils.theme as theme
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_loading_spinners as dls
from dash import callback

df = pd.read_csv("../../preprocessed_match_data.csv")

TeamGoalsStats = html.Div(className="card-chart-container col-lg-4 md-6 sm-12",
                          children=[
                              html.Div(
                                  className="card-chart",
                                  children=[
                                      html.H4("Scored vs. Conceded  Goals",
                                              className="card-header card-m-0 me-2 pb-3"),
                                      dls.Triangle(
                                          id="team-goals-stats",
                                          debounce=theme.LOADING_DEBOUNCE
                                      )
                                  ]
                              )

                          ],
                          )


@callback(
    Output("team-goals-stats", "children"),
    Input("query-team-select", "value"),
    State("team-stats-df", "data")
)
def update_team_goals_stats(selected_team, selected_season):
    if selected_team is None or selected_season is None:
        return []

    filtered_df = df[(df["team"] == selected_team) &
                     (df["season"] == selected_season)]

    total_goals = filtered_df["gf"].sum()
    goals_against = filtered_df["ga"].sum()

    return dcc.Graph(figure=px.bar(x=["Goals Scored", "Goals goals_against"], y=[total_goals, goals_conceded], height=theme.MAX_CHART_HEIGHT,
                                   labels={"y": "Count", "x": ""}, color_discrete_sequence=theme.COLOR_PALLETE, text_auto=True,
                                   ).update_layout(paper_bgcolor="rgb(0,0,0,0)",
                                                   plot_bgcolor="rgb(0,0,0,0)",
                                                   legend=dict(
                                                       bgcolor=theme.LEGEN_BG),
                                                   font_family=theme.FONT_FAMILY,
                                                   ),
                     config={
        "displayModeBar": False},
        style=theme.CHART_STYLE

    )
