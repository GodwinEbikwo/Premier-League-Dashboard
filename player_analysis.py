# import dash
# from dash import dcc, html, callback
# from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objs as go

# player_df = pd.read_csv("clean_player_data.csv")

# head_to_head_page_content = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.Label("Select Season:"),
#             dcc.Dropdown(
#                 id='season-dropdown',
#                 options=[{'label': s, 'value': s}
#                          for s in player_df['season'].unique()],
#                 value=None
#             )
#         ], width=6),
#         dbc.Col([
#             html.Label("Select Player 1:"),
#             dcc.Dropdown(
#                 id="player1-dropdown",
#                 options=[{'label': player, 'value': player}
#                          for player in player_df['player'].unique()],
#                 value=None,
#                 multi=False
#             )
#         ], width=6),
#         dbc.Col([
#             html.Label("Select Player 2:"),
#             dcc.Dropdown(
#                 id="player2-dropdown",
#                 options=[{'label': player, 'value': player}
#                          for player in player_df['player'].unique()],
#                 value=None,
#                 multi=False
#             )
#         ], width=6)
#     ]),
#     html.Div(id="player-comparison-output")
# ])


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
#         style={'margin': '20px'}
#     )

#     return card


# @callback(
#     Output("player-comparison-output", "children"),
#     Input("player1-dropdown", "value"),
#     Input("player2-dropdown", "value"),
#     Input('season-dropdown', 'value')
# )
# def update_player_comparison(player1, player2, selected_season):
#     if player1 is None or player2 is None:
#         return html.Div("Select two players to compare.")

#     # Filter the player DataFrame for the selected players
#     player1_data = player_df[(player_df['player'] == player1) & (
#         player_df['season'] == selected_season)]
#     player2_data = player_df[(player_df['player'] == player2) & (
#         player_df['season'] == selected_season)]

#     if player1_data.empty or player2_data.empty:
#         return html.Div("Selected players or season not found in the dataset. Please choose different players or season.")

#     player_1_card = generate_player_card(
#         player1, player1_data, selected_season)
#     player_2_card = generate_player_card(
#         player2, player2_data, selected_season)

#     cards_row = dbc.Row([
#         dbc.Col(player_1_card, width=6),
#         dbc.Col(player_2_card, width=6)
#     ])

#     return cards_row


import dash
from dash import dcc, html, State, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go

player_df = pd.read_csv("clean_player_data.csv")

offcanvas_content = dbc.Row([
    dbc.Col([
            html.Label("Select Season:"),
            dcc.Dropdown(
                id='season-dropdown',
                options=[{'label': s, 'value': s}
                         for s in player_df['season'].unique()],
                value=None
            )
            ], width=6),
    dbc.Col([
            html.Label("Select Player 1:"),
            dcc.Dropdown(
                id="player1-dropdown",
                options=[{'label': player, 'value': player}
                         for player in player_df['player'].unique()],
                value=None,
                multi=False
            )
            ], width=6),
    dbc.Col([
            html.Label("Select Player 2:"),
            dcc.Dropdown(
                id="player2-dropdown",
                options=[{'label': player, 'value': player}
                         for player in player_df['player'].unique()],
                value=None,
                multi=False
            )
            ], width=6)
]),

offcanvas = html.Div(
    [
        dbc.Button(
            "Open Offcanvas", id="open-offcanvas-placement", n_clicks=0
        ),
        dbc.Offcanvas(
            offcanvas_content,
            id="offcanvas-placement",
            title="Placement",
            placement="end",  # Set the default placement to 'end'
            is_open=False,
        ),
    ]
)


head_to_head_page_content = dbc.Container([
    offcanvas,  # Add the OpenCanvas component here
    html.Div(id="player-comparison-output")
])


def generate_player_card(player, player_data, selected_season):
    summary_items = [
        html.P(f"{player} in {selected_season}", style={
               'font-weight': 'bold', 'font-size': '18px'})
    ]

    fields = {
        'age': 'Age',
        'nation': 'Nationality',
        'pos': 'Position',
        'gls': 'Goals',
        'ast': 'Assists',
        'starts': 'Matches Started',
        'min': 'Minutes Played',
        'g-pk': 'Non Penalty Goals',
        'crdr': 'Red Cards',
        'crdy': 'Yellow Cards'
    }

    for field, label in fields.items():
        if field in player_data:
            summary_items.append(
                html.P(f"{label}: {player_data[field].values[0]}"))

    summary_content = html.Div(summary_items)

    card = dbc.Card(
        dbc.CardBody(summary_content),
        style={'margin': '20px'}
    )

    return card


@callback(
    Output("player-comparison-output", "children"),
    Input("player1-dropdown", "value"),
    Input("player2-dropdown", "value"),
    Input('season-dropdown', 'value')
)
def update_player_comparison(player1, player2, selected_season):
    if player1 is None or player2 is None:
        return html.Div("Select two players to compare.")

    # Filter the player DataFrame for the selected players
    player1_data = player_df[(player_df['player'] == player1) & (
        player_df['season'] == selected_season)]
    player2_data = player_df[(player_df['player'] == player2) & (
        player_df['season'] == selected_season)]

    if player1_data.empty or player2_data.empty:
        return html.Div("Selected players or season not found in the dataset. Please choose different players or season.")

    player_1_card = generate_player_card(
        player1, player1_data, selected_season)
    player_2_card = generate_player_card(
        player2, player2_data, selected_season)

    cards_row = dbc.Row([
        dbc.Col(player_1_card, width=6),
        dbc.Col(player_2_card, width=6)
    ])

    return cards_row


@callback(
    Output("offcanvas-placement", "is_open"),
    Input("open-offcanvas-placement", "n_clicks"),
    [State("offcanvas-placement", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@callback(
    Output("offcanvas-placement", "placement"),
    Input("offcanvas-placement-selector", "value"),
)
def toggle_placement(placement):
    return placement
