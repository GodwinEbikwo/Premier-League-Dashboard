import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pandas as pd

BASE_URL = "https://fbref.com"
headers = {
    'User-Agent': 'Your User Agent',  # Replace with an actual User-Agent string
    # Add more headers as needed
}


def get_squad_misc_stats(base_url, season):
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
                CrdY = columns[3].get_text(
                ) if columns[3].get_text() != '' else None
                CrdR = columns[4].get_text(
                ) if columns[4].get_text() != '' else None
                Fls = columns[5].get_text()
                Crs = columns[9].get_text()
                Int = columns[10].get_text()
                OG = columns[14].get_text()

                data.append([team_name, CrdY, CrdR, Fls, Crs, Int, OG, season])
    else:
        print("Squad Miscellaneous Stats table not found.")

    return data


if __name__ == "__main__":
    seasons = list(range(2021, 2020, -1))
    print(seasons)
    all_data = []

    for season in seasons:
        season_data = get_squad_misc_stats(
            BASE_URL + f"/en/comps/9/{season}-{season+1}/{season}-{season+1}-Premier-League-Stats", season)
        all_data.extend(season_data)

    # Create a pandas DataFrame from the collected data with lowercase column names
    columns = ['team', 'yellow_cards', 'red_cards', 'fouls_committed',
               'crosses', 'interceptions', 'own_goals', 'season']
    df = pd.DataFrame(all_data, columns=columns)

    # Convert certain columns to appropriate data types
    df['yellow_cards'] = pd.to_numeric(df['yellow_cards'], errors='coerce')
    df['red_cards'] = pd.to_numeric(df['red_cards'], errors='coerce')

    # Fill missing values in numeric columns with zeros
    numeric_cols = ['yellow_cards', 'red_cards']
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Save DataFrame to a CSV file
    df.to_csv('new_squad_misc_stats.csv', index=False)

    print("Data saved to squad_misc_stats.csv")
