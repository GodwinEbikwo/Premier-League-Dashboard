# from dash import dcc, html, State, Input, Output, callback
# import dash_bootstrap_components as dbc
# import pandas as pd

# player_df = pd.read_csv("clean_player_data.csv")

# # First canvas dropdowns
# offcanvas1_content = dbc.Row([
#     dbc.Col([
#         html.Label("Select Season:"),
#         dcc.Dropdown(
#             id='season-dropdown-canvas1',
#             options=[{'label': s, 'value': s}
#                      for s in player_df['season'].unique()],
#             value=None
#         )
#     ], width=6),
#     dbc.Col([
#         html.Label("Select Player 1:"),
#         dcc.Dropdown(
#             id="player1-dropdown-canvas1",
#             options=[{'label': player, 'value': player}
#                      for player in player_df['player'].unique()],
#             value=None,
#             multi=False
#         )
#     ], width=6)
# ])

# # Second canvas dropdowns
# offcanvas2_content = dbc.Row([
#     dbc.Col([
#         html.Label("Select Season:"),
#         dcc.Dropdown(
#             id='season-dropdown-canvas2',
#             options=[{'label': s, 'value': s}
#                      for s in player_df['season'].unique()],
#             value=None
#         )
#     ], width=6),
#     dbc.Col([
#         html.Label("Select Player 2:"),
#         dcc.Dropdown(
#             id="player1-dropdown-canvas2",
#             options=[{'label': player, 'value': player}
#                      for player in player_df['player'].unique()],
#             value=None,
#             multi=False
#         )
#     ], width=6)
# ])

# # First canvas Offcanvas
# offcanvas1 = html.Div(
#     [
#         dbc.Button(
#             [html.I(className="bi bi-plus-circle me-2"),
#              "Add a player for Canvas 1"],
#             id="open-offcanvas-canvas1",
#             n_clicks=0,
#             outline=True,
#         ),
#         dbc.Offcanvas(
#             offcanvas1_content,
#             id="offcanvas-canvas1",
#             title="Canvas 1",
#             placement="end",
#             is_open=False,
#         ),
#     ],
#     className="button_group d-flex justify-content-center align-items-center"
# )

# # Second canvas Offcanvas
# offcanvas2 = html.Div(
#     [
#         dbc.Button(
#             [html.I(className="bi bi-plus-circle me-2"),
#              "Add a player for Canvas 2"],
#             id="open-offcanvas-canvas2",
#             n_clicks=0,
#             outline=True,
#         ),
#         dbc.Offcanvas(
#             offcanvas2_content,
#             id="offcanvas-canvas2",
#             title="Canvas 2",
#             placement="end",
#             is_open=False,
#         ),
#     ],
#     className="button_group d-flex justify-content-center align-items-center"
# )


# def generate_player_card(player, player_data, selected_season):
#     summary_items = [
#         html.P(f"{player} in {selected_season}", style={
#                'font-weight': 'bold', 'font-size': '18px'})
#     ]

#     fields = {
#         'age': 'Age',
#         'nation': 'Nationality',
#         'pos': 'Position',
#         'gls': 'Goals',
#         'ast': 'Assists',
#         'starts': 'Matches Started',
#         'min': 'Minutes Played',
#         'g-pk': 'Non Penalty Goals',
#         'crdr': 'Red Cards',
#         'crdy': 'Yellow Cards'
#     }

#     for field, label in fields.items():
#         if field in player_data:
#             summary_items.append(
#                 html.P(f"{label}: {player_data[field].values[0]}"))

#     summary_content = html.Div(summary_items)

#     card = dbc.Card(
#         dbc.CardBody(summary_content),
#         style={'margin-top': '10px'}
#     )

#     return card


# @callback(
#     Output("player-comparison-output", "children"),
#     Input("player1-dropdown-canvas1", "value"),
#     Input("player1-dropdown-canvas2", "value"),
#     Input("season-dropdown-canvas1", "value"),
#     Input("season-dropdown-canvas2", "value"),
# )
# def update_player_comparison(player1_canvas1, player1_canvas2, season_canvas1, season_canvas2):
#     player_cards = []

#     def generate_player_card_div(player, player_data, selected_season):
#         player_card = generate_player_card(
#             player, player_data, selected_season)
#         return dbc.Col(player_card, width=6)

#     if player1_canvas1 and season_canvas1:
#         player1_data = player_df[(player_df['player'] == player1_canvas1) & (
#             player_df['season'] == season_canvas1)]
#         if not player1_data.empty:
#             player_cards.append(
#                 generate_player_card_div(player1_canvas1, player1_data, season_canvas1))

#     if player1_canvas2 and season_canvas2:
#         player1_data = player_df[(player_df['player'] == player1_canvas2) & (
#             player_df['season'] == season_canvas2)]
#         if not player1_data.empty:
#             player_cards.append(
#                 generate_player_card_div(player1_canvas2, player1_data, season_canvas2))

#     return dbc.Row(player_cards)


# @callback(
#     Output("offcanvas-canvas1", "is_open"),
#     Input("open-offcanvas-canvas1", "n_clicks"),
#     [State("offcanvas-canvas1", "is_open")],
# )
# def toggle_offcanvas_canvas1(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open


# @callback(
#     Output("offcanvas-canvas2", "is_open"),
#     Input("open-offcanvas-canvas2", "n_clicks"),
#     [State("offcanvas-canvas2", "is_open")],
# )
# def toggle_offcanvas_canvas2(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open


# head_to_head_page_content = dbc.Container([
#     html.Div([
#         dbc.Row([
#             dbc.Col(
#                 [offcanvas1],  width=6,
#             ),
#             dbc.Col(
#                 [offcanvas2],  width=6,
#             )
#         ], className="d-flex flex-row justify-content-center align-items-center")
#     ]),
#     html.Div(id="player-comparison-output")
# ])


import pandas as pd
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

player_df = pd.read_csv("./data/player_df.csv")
player_df.drop_duplicates(inplace=True)

head_to_head_page_content = html.Div([
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='team-dropdown',
            options=[{'label': t, 'value': t}
                for t in player_df['team'].unique()],
            value=player_df['team'].iloc[0]
        )),
        dbc.Col(dcc.Dropdown(
            id='team-dropdown-2',
            options=[{'label': t, 'value': t}
                for t in player_df['team'].unique()],
            value=player_df['team'].iloc[0]
        )),
    ], style={'margin-bottom': '10px'}),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='season-dropdown',
            options=[{'label': s, 'value': s}
                for s in player_df['season'].unique()],
            value=player_df['season'].iloc[0]
        )),
    ], style={'margin-bottom': '10px'}),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='player-dropdown',
            options=[{'label': p, 'value': p}
                for p in player_df['player'].unique()],
            value=player_df['player'].iloc[0]
        )),
        dbc.Col(dcc.Dropdown(
            id='player-dropdown-2',
            options=[{'label': p, 'value': p}
                for p in player_df['player'].unique()],
            multi=False,
            placeholder="Select Player 2"
        )),
    ]),
    html.Div(id='player-summary'),
    dcc.Graph(id='radar-chart'),
    dcc.Graph(id='comparison-bar-chart')
])


@callback(
    Output('team-dropdown-2', 'options'),
    [Input('season-dropdown', 'value')]
)
def update_teams_dropdown(selected_season):
    if not selected_season:
        return []

    # Filter teams based on the selected season
    teams_for_season = player_df[player_df['season']
                                 == selected_season]['team'].unique()

    team_options = [{'label': team, 'value': team}
                    for team in teams_for_season]

    return team_options


@callback(
    Output('team-dropdown-2', 'value'),
    [Input('season-dropdown', 'value')]
)
def update_team_dropdown_2_value(selected_season):
    if not selected_season:
        return None

    # Get the first available team for the selected season
    teams_for_season = player_df[player_df['season']
                                 == selected_season]['team'].unique()

    if len(teams_for_season) > 0:
        return teams_for_season[1]

    return None


@callback(
    [Output('player-dropdown', 'options'),
     Output('player-dropdown', 'value'),
     Output('player-dropdown-2', 'options'),
     Output('player-dropdown-2', 'value')],
    [Input('team-dropdown', 'value'),
     Input('team-dropdown-2', 'value'),
     Input('season-dropdown', 'value')]
)
def update_players_and_value(selected_team_1, selected_team_2, selected_season):
    if not selected_team_1 or not selected_team_2:
        return [], None, [], None

    selected_1 = player_df[(player_df['team'] == selected_team_1) & (
        player_df['season'] == selected_season)]
    selected_2 = player_df[(player_df['team'] == selected_team_2) & (
        player_df['season'] == selected_season)]

    player_options_1 = [{'label': p, 'value': p}
                        for p in selected_1['player'].unique()]
    player_options_2 = [{'label': p, 'value': p}
                        for p in selected_2['player'].unique()]

    return player_options_1, player_options_1[0]['value'], player_options_2, player_options_2[1]['value']


def generate_player_card(player, player_data, selected_season):
    img_url = player_data['img_url'].values[0]
    img_tag = html.Img(src=img_url, alt=player, style={'max-width': '100px'})

    fields = {
        'age': 'Age',
        'pos': 'Position',
        'nation': 'Nationality',
    }

    performance = {
        'gls': 'Goals',
        'ast': 'Assists',
        'g+a': 'Goals + Assists',
        'g-pk': 'Non Penalty Goals',
        'crdr': 'Red Cards',
        'crdy': 'Yellow Cards',
        'pkatt': 'Penalty kicks attempted'
    }

    # Create separate lists for summary and performance sections
    summary_content = [
        html.Div(img_tag, className="img_styles"),
        html.Hr(),
        html.H2(f"{player} in {selected_season}", style={
                'font-weight': 'bold'}),
        html.Hr(),
        html.H6("Overview"),
        html.Hr(),
        *[html.P(f"{label}: {player_data[field].values[0]}")
          for field, label in fields.items()
          if field in player_data]
    ]

    performance_content = [
        html.H6("Performance"),
        html.Hr(),
        *[
            html.P(f"{label}: {player_data[field].values[0]}")
            for field, label in performance.items()
            if field in player_data
        ]
    ]

    # Wrap the content lists in separate div elements
    summary_content = html.Div(summary_content)
    performance_content = html.Div(performance_content)

    card = dbc.Card(
        [
            dbc.CardBody(summary_content, style={'padding': '0 1rem'}),
            dbc.CardBody(performance_content, style={'padding': '0 1rem'})
        ],
        style={'margin': '10px 0px'}
    )

    return card


@callback(
    Output('player-summary', 'children'),
    [Input('player-dropdown', 'value'),
     Input('player-dropdown-2', 'value'),
     Input('season-dropdown', 'value')]
)
def update_summary(player_1, player_2, selected_season):
    if not player_1 or not player_2:
        return html.P("Please select players from both teams to compare.")

    player_data_1 = player_df[(player_df['player'] == player_1) & (
        player_df['season'] == selected_season)]
    player_data_2 = player_df[(player_df['player'] == player_2) & (
        player_df['season'] == selected_season)]

    player_1_card = generate_player_card(
        player_1, player_data_1, selected_season)
    player_2_card = generate_player_card(
        player_2, player_data_2, selected_season)

    cards_row = dbc.Row([
        dbc.Col(player_1_card, width=6),
        dbc.Col(player_2_card, width=6)
    ])

    return cards_row


@callback(
    Output('radar-chart', 'figure'),
    [Input('player-dropdown', 'value'),
     Input('player-dropdown-2', 'value'),
     Input('season-dropdown', 'value')]
)
def update_radar_chart(player_1, player_2, selected_season):
    if not player_1 or not player_2:
        return go.Figure()

    # Filter data for the selected players and season
    player_data_1 = player_df[(player_df['player'] == player_1) & (
        player_df['season'] == selected_season)]
    player_data_2 = player_df[(player_df['player'] == player_2) & (
        player_df['season'] == selected_season)]

    if player_data_1.empty or player_data_2.empty:
        return go.Figure()

    # Define the statistics to be included in the radar chart
    categories = ['gls', 'ast', 'g+a', 'g-pk', 'crdr', 'crdy', 'pkatt']

    # Extract the values for each player
    player_1_values = [player_data_1.iloc[0][stat] for stat in categories]
    player_2_values = [player_data_2.iloc[0][stat] for stat in categories]

    # Create the radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=player_1_values,
        theta=categories,
        fill='toself',
        name=player_1
    ))

    fig.add_trace(go.Scatterpolar(
        r=player_2_values,
        theta=categories,
        fill='toself',
        name=player_2
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                # Set the range of values on the radial axis
                range=[0, max(max(player_1_values), max(player_2_values)) + 2]
            )),
        showlegend=True
    )

    return fig


@callback(
    Output('comparison-bar-chart', 'figure'),
    [Input('player-dropdown', 'value'),
     Input('player-dropdown-2', 'value'),
     Input('season-dropdown', 'value')]
)
def update_bar_chart(player_1, player_2, selected_season):
    if not player_1 or not player_2:
        return go.Figure()

    # Filter data for the selected players and season
    player_data_1 = player_df[(player_df['player'] == player_1) & (
        player_df['season'] == selected_season)]
    player_data_2 = player_df[(player_df['player'] == player_2) & (
        player_df['season'] == selected_season)]

    if player_data_1.empty or player_data_2.empty:
        return go.Figure()

    # Define the statistics to be included in the bar chart
    categories = ['gls', 'ast', 'g+a', 'g-pk', 'crdr', 'crdy', 'pkatt']

    # Extract the values for each player
    player_1_values = [player_data_1.iloc[0][stat] for stat in categories]
    player_2_values = [player_data_2.iloc[0][stat] for stat in categories]

    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(name=player_1, x=categories, y=player_1_values),
        go.Bar(name=player_2, x=categories, y=player_2_values)
    ])

    # Customize the layout
    fig.update_layout(
        barmode='group',
        xaxis_title='Statistics',
        yaxis_title='Values',
        title='Player Comparison',
        title_x=0.5,
        xaxis=dict(tickvals=list(range(len(categories))), ticktext=categories),
        yaxis=dict(title='Value'),
        legend=dict(title='Players', orientation="h",
                    yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


# @callback(
#     Output('radar-chart', 'figure'),
#     [Input('player-dropdown', 'value'),
#      Input('player-dropdown-2', 'value'),
#      Input('season-dropdown', 'value')]
# )
# def update_radar_chart(player_1, player_2, selected_season):
#     if not player_1 or not player_2:
#         return go.Figure()

#     player_data_1 = player_df[(player_df['player'] == player_1) & (
#         player_df['season'] == selected_season)]
#     player_data_2 = player_df[(player_df['player'] == player_2) & (
#         player_df['season'] == selected_season)]

#     # Extract relevant attributes for radar chart
#     attributes = ['age', 'gls', 'ast', 'starts', 'min', 'prgc', 'prgp']

#     values_1 = player_data_1[attributes].values[0]
#     values_2 = player_data_2[attributes].values[0]

#     maxxx = range = [0, max(max(values_1), max(values_2))]

#     fig = go.Figure()

#     fig.add_trace(go.Scatterpolar(
#         r=values_1,
#         theta=attributes,
#         fill='toself',
#         name=player_1
#     ))

#     fig.add_trace(go.Scatterpolar(
#         r=values_2,
#         theta=attributes,
#         fill='toself',
#         name=player_2
#     ))

#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(visible=True, range=[0, 100])
#         ),
#         showlegend=True
#     )

#     return fig
