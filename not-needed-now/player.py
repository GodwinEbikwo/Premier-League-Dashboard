# import seaborn as sns
# import matplotlib.pyplot as plt
# import pandas as pd

# pl_upto20 = pd.read_csv("clean_player_data.csv")
# print(pl_upto20.info())

# # Filter the data for the 2022 season
# season_2022_data = pl_upto20[pl_upto20['season'] == 2022]

# # Group by team and calculate the sum of goals scored
# team_goals = season_2022_data.groupby('team')['gls'].sum()

# # Identify the team with the highest sum of goals
# team_with_most_goals = team_goals.idxmax()


# # Filter out rows with unwanted player names
# filtered_data = season_2022_data[
#     ~season_2022_data['player'].isin(['Opponent Total', 'Squad Total'])
# ]

# # Calculate the sum of goals for each player and find the top 10
# player_most_goals = filtered_data.groupby('player')['gls'].sum().nlargest(10)

# print(player_most_goals)

# # print(player_most_goals)

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

pl_upto20 = pd.read_csv("clean_player_data.csv")
print(pl_upto20.info())

# Filter the data for the 2022 season
season_2022_data = pl_upto20[pl_upto20['season'] == 2022]


# Filter out rows with unwanted player names
filtered_data = season_2022_data[
    ~season_2022_data['player'].isin(['Opponent Total', 'Squad Total'])
]

# Calculate the sum of goals for each player and find the top 10
player_most_goals = filtered_data.groupby('player')['gls'].sum().nlargest(10)

print(player_most_goals)

# print(player_most_goals)
