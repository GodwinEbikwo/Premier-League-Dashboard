import pandas as pd

# misc_df = pd.read_csv("./data/squad_misc_df.csv")
# player_df = pd.read_csv("./data/player_df.csv")

player_df = pd.read_csv("./data/player_df.csv")


def calculate_team_top_scorers(player_df, selected_team, selected_season):
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


# print(top_scorers)
# player_img_df = pd.read_csv("./data/player_img_df.csv")


# # drop these columns from the player_df
# player_df.drop(player_df.columns[23:33], axis=1, inplace=True)

# # handle the missing data in player_img_df
# player_img_df.dropna(subset=['img_url'], inplace=True)

# merged_df = player_df.merge(player_img_df, on='player', how='inner')

# columns_to_drop = ['matches', 'npxg+xag',]

# merged_df.drop(columns_to_drop, axis=1, inplace=True)


# merged_df.to_csv('./data/merged_data.csv', index=False)

# Check for complete duplicates across all columns


# Uncomment the line below if you want to proceed with the DataFrame without full row duplicates
# player_df = player_df_no_full_row_duplicates
# duplicates = player_df[player_df.duplicated()]
# print("Full row duplicates:")
# print(duplicates)
player_df.drop_duplicates(inplace=True)


selected_team = "Arsenal"
# Use a string if you've converted the 'season' column to string, otherwise an integer.
selected_season = "2022"
top_scorers = calculate_team_top_scorers(
    player_df, selected_team, selected_season)


print(player_df.info())

print(top_scorers)

# print(player_df.duplicated().sum())
