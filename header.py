from dash import dcc, html
import dash_bootstrap_components as dbc


def Header(df):
    return html.Div([
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
        ])
    ])
