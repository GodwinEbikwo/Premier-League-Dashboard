import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from requests.exceptions import RequestException
SHOOTING_COLUMNS = ['Date', 'Sh', 'SoT', 'Dist', 'FK', 'PK', 'PKatt']

BASE_URL = "https://fbref.com"
years = list(range(2022, 2014, -1))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


def get_team_urls(base_url):
    """Get team squad page URLs from FBRef standings page"""

    # ensure wer have a BASE_URL
    if not base_url:
        raise ValueError("base_url is required")

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
    except RequestException as err:
        raise RuntimeError(
            f"Error occured when fetching {base_url}: {err}") from err

    # initializing the soup object
    soup = BeautifulSoup(response.content, 'html.parser')
    standings_table = soup.select_one('table.stats_table')

    # get all a tag elements in the standings_table
    # then only get links that have the squad in it
    links = [a['href'] for a in standings_table.select('a[href*="/squad"]')]
    team_urls = [f"{BASE_URL}{link}" for link in links]

    return team_urls, response


def get_shooting_link(team_url):
    """Get shooting data link for a team"""

    if not team_url:
        raise ValueError("team_url is required")

    try:
        response = requests.get(team_url, headers=headers)
        response.raise_for_status()
    except RequestException as err:
        raise RuntimeError(f"Error fetching {team_url}: {err}") from err

    soup = BeautifulSoup(response.content, "html.parser")
    shooting_link = next((a["href"] for a in soup.find_all(
        "a") if "all_comps/shooting" in a.get("href", "")), None)

    if not shooting_link:
        raise ValueError(f"No shooting link found for {team_url}")

    return {"team_url": team_url, "shooting_link": f"https://fbref.com{shooting_link}"}


if __name__ == "__main__":
    all_matches = []
    all_player_stats = []

    for year in years:
        team_urls, _ = get_team_urls(
            BASE_URL + f"/en/comps/9/{year}-{year+1}/{year}-{year+1}-Premier-League-Stats")

        for team_url in team_urls:
            team_name = team_url.split(
                "/")[-1].replace("-Stats", "").replace("-", " ")
            print(team_url)

            try:
                team_data = requests.get(team_url)
                team_data.raise_for_status()

                players_data = pd.read_html(
                    team_data.text, match="Standard Stats")[0]
                matches = pd.read_html(
                    team_data.text, match="Scores & Fixtures")[0]

                players_data.columns = players_data.columns.droplevel()
                players_data.columns = [c.lower()
                                        for c in players_data.columns]

                shooting_link_data = get_shooting_link(team_url)
                shooting_data = requests.get(
                    shooting_link_data["shooting_link"])
                shooting = pd.read_html(
                    shooting_data.text, match="Shooting")[0]
                shooting.columns = shooting.columns.droplevel()

                for col in SHOOTING_COLUMNS:
                    if col not in shooting.columns:
                        shooting[col] = pd.NA

                team_data = matches.merge(
                    shooting[SHOOTING_COLUMNS], on="Date")
                team_data = team_data[team_data["Comp"] == 'Premier League']

                team_data['Team'] = team_name
                team_data['Season'] = year
                all_matches.append(team_data)

                # Store player stats for later merging
                players_data['Team'] = team_name
                players_data['Season'] = year
                all_player_stats.append(players_data)

                time.sleep(10)

            except (RequestException, ValueError, IndexError, pd.errors.EmptyDataError) as err:
                print(f"Error processing {team_name} ({year}): {err}")
                continue

    # Reset index for all player stats DataFrames
    for i in range(len(all_player_stats)):
        all_player_stats[i].reset_index(drop=True, inplace=True)

    match_df = pd.concat(all_matches)
    match_df.columns = [c.lower() for c in match_df.columns]
    match_df.to_csv("A-scrapped_games-19th-Aug.csv", index=False)

    player_df = pd.concat(all_player_stats, ignore_index=True)
    player_df.to_csv("A-scrapped_player_stats-19th-Aug.csv", index=False)
