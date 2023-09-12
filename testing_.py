import pandas as pd

player_df = pd.read_csv("./data/player_df.csv")
player_img_df = pd.read_csv("./data/player_img_df.csv")


# drop these columns from the player_df
player_df.drop(player_df.columns[23:33], axis=1, inplace=True)

# handle the missing data in player_img_df
player_img_df.dropna(subset=['img_url'], inplace=True)

merged_df = player_df.merge(player_img_df, on='player', how='inner')

columns_to_drop = ['matches', 'npxg+xag',]

merged_df.drop(columns_to_drop, axis=1, inplace=True)


merged_df.to_csv('./data/merged_data.csv', index=False)
