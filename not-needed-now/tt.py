# import random
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# import time
# from requests.exceptions import RequestException
# SHOOTING_COLUMNS = ['Date', 'Sh', 'SoT', 'Dist', 'FK', 'PK', 'PKatt']

# BASE_URL = "https://fbref.com"
# years = list(range(2022, 2021, -1))

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
# }


# def get_team_urls(base_url):
#     """Get team squad page URLs from FBRef standings page"""

#     # ensure wer have a BASE_URL
#     if not base_url:
#         raise ValueError("base_url is required")

#     try:
#         response = requests.get(base_url, headers=headers)
#         response.raise_for_status()
#     except RequestException as err:
#         raise RuntimeError(
#             f"Error occured when fetching {base_url}: {err}") from err

#     # initializing the soup object
#     soup = BeautifulSoup(response.content, 'html.parser')
#     standings_table = soup.select_one('table.stats_table')

#     # get all a tag elements in the standings_table
#     # then only get links that have the squad in it
#     links = [a['href'] for a in standings_table.select('a[href*="/squad"]')]
#     team_urls = [f"{BASE_URL}{link}" for link in links]

#     return team_urls, response


# def get_shooting_link(team_url):
#     """Get shooting data link for a team"""

#     if not team_url:
#         raise ValueError("team_url is required")

#     try:
#         response = requests.get(team_url, headers=headers)
#         response.raise_for_status()
#     except RequestException as err:
#         raise RuntimeError(f"Error fetching {team_url}: {err}") from err

#     soup = BeautifulSoup(response.content, "html.parser")
#     shooting_link = next((a["href"] for a in soup.find_all(
#         "a") if "all_comps/shooting" in a.get("href", "")), None)

#     if not shooting_link:
#         raise ValueError(f"No shooting link found for {team_url}")

#     return {"team_url": team_url, "shooting_link": f"https://fbref.com{shooting_link}"}


# if __name__ == "__main__":
#     all_matches = []
#     all_player_stats = []

#     for year in years:
#         team_urls, _ = get_team_urls(
#             BASE_URL + f"/en/comps/9/{year}-{year+1}/{year}-{year+1}-Premier-League-Stats")

#         for team_url in team_urls:
#             team_name = team_url.split(
#                 "/")[-1].replace("-Stats", "").replace("-", " ")
#             print(team_url)

#             try:
#                 team_data = requests.get(team_url)
#                 team_data.raise_for_status()

#             except (RequestException, ValueError, IndexError, pd.errors.EmptyDataError) as err:
#                 print(f"Error processing {team_name} ({year}): {err}")
#                 continue

#     #             players_data = pd.read_html(
#     #                 team_data.text, match="Standard Stats")[0]
#     #             matches = pd.read_html(
#     #                 team_data.text, match="Scores & Fixtures")[0]

#     #             players_data.columns = players_data.columns.droplevel()
#     #             players_data.columns = [c.lower()
#     #                                     for c in players_data.columns]

#     #             shooting_link_data = get_shooting_link(team_url)
#     #             shooting_data = requests.get(
#     #                 shooting_link_data["shooting_link"])
#     #             shooting = pd.read_html(
#     #                 shooting_data.text, match="Shooting")[0]
#     #             shooting.columns = shooting.columns.droplevel()

#     #             for col in SHOOTING_COLUMNS:
#     #                 if col not in shooting.columns:
#     #                     shooting[col] = pd.NA

#     #             team_data = matches.merge(
#     #                 shooting[SHOOTING_COLUMNS], on="Date")
#     #             team_data = team_data[team_data["Comp"] == 'Premier League']

#     #             team_data['Team'] = team_name
#     #             team_data['Season'] = year
#     #             all_matches.append(team_data)

#     #             # Store player stats for later merging
#     #             players_data['Team'] = team_name
#     #             players_data['Season'] = year
#     #             all_player_stats.append(players_data)

#     #             time.sleep(10)

#     #         except (RequestException, ValueError, IndexError, pd.errors.EmptyDataError) as err:
#     #             print(f"Error processing {team_name} ({year}): {err}")
#     #             continue

#     # # Reset index for all player stats DataFrames
#     # for i in range(len(all_player_stats)):
#     #     all_player_stats[i].reset_index(drop=True, inplace=True)

#     # match_df = pd.concat(all_matches)
#     # match_df.columns = [c.lower() for c in match_df.columns]
#     # match_df.to_csv("A-scrapped_games-19th-Aug.csv", index=False)

#     # player_df = pd.concat(all_player_stats, ignore_index=True)
#     # player_df.to_csv("A-scrapped_player_stats-19th-Aug.csv", index=False)

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pandas as pd

BASE_URL = "https://fbref.com"
headers = {
    'User-Agent': 'Your User Agent',  # Replace with an actual User-Agent string
    # Add more headers as needed
}


def get_squad_misc_stats(base_url):
    """Get squad miscellaneous stats from FBRef standings page"""

    data = []  # List to store extracted data

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except RequestException as err:
        raise RuntimeError(
            f"Error occurred when fetching {base_url}: {err}") from err

    soup = BeautifulSoup(response.content, 'html.parser')
    squad_misc_table = soup.find('table', {'id': 'stats_squads_misc_for'})

    if squad_misc_table:
        rows = squad_misc_table.find_all('tr')
        for row in rows[2:]:
            columns = row.find_all(['th', 'td'])
            if columns:
                team_name = columns[0].get_text()
                CrdY = columns[3].get_text()
                CrdR = columns[4].get_text()
                Fls = columns[6].get_text()
                Crs = columns[9].get_text()
                Int = columns[10].get_text()
                PKWon = columns[12].get_text()
                OG = columns[14].get_text()

                data.append([team_name, CrdY, CrdR, Fls, Crs, Int, PKWon, OG])
    else:
        print("Squad Miscellaneous Stats table not found.")

    return data


if __name__ == "__main__":
    seasons = list(range(2022, 2016, -1))
    print(seasons)
    all_data = []

    for season in seasons:
        season_data = get_squad_misc_stats(
            BASE_URL + f"/en/comps/9/{season}-{season+1}/{season}-{season+1}-Premier-League-Stats")

        for row in season_data:
            row.append(season)
        all_data.extend(season_data)

    # # Create a pandas DataFrame from the collected data
    columns = ['Team', 'Yellow_Card', 'Red_Card',
               'Fouls_Committed', 'Crosses', 'Interceptions', 'PKWon', 'Own_Goals', 'Season']
    df = pd.DataFrame(all_data, columns=columns)

    # Convert certain columns to appropriate data types
    df['Yellow_Card'] = pd.to_numeric(df['Yellow_Card'], errors='coerce')
    df['Red_Card'] = pd.to_numeric(df['Red_Card'], errors='coerce')

    # Fill missing values in numeric columns with zeros
    numeric_cols = ['Yellow_Card', 'Red_Card']
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # # covert it col names to lowercase
    df.columns = [c.lower() for c in df.columns]

    # # Save DataFrame to a CSV file
    df.to_csv('squad_misc_stats.csv', index=False)

    print("Data saved to squad_misc_stats.csv")
