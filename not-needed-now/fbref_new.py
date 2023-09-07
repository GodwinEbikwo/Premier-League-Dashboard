# import time
# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from requests.exceptions import RequestException

# BASE_URL = "https://fbref.com"
# standings_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"
# years = list(range(2022, 2020, -1))
# all_matches = []

# if __name__ == "__main__":
#     for year in years:
#         try:
#             response = requests.get(standings_URL)
#             response.raise_for_status()
#         except RequestException as err:
#             raise RuntimeError(
#                 f"Error occured when fetching {standings_URL}: {err}") from err
#         # initializing the soup object
#         soup = BeautifulSoup(response.content, 'html.parser')
#         standings_table = soup.select_one('table.stats_table')

#         # get all a tag elements in the standings_table
#         # then only get links that have the squad in it
#         links = [a['href']
#                  for a in standings_table.select('a[href*="/squad"]')]
#         team_urls = [f"{BASE_URL}{link}" for link in links]

#         previous_season = soup.select("a.prev")[0].get("href")
#         standings_URL = f"{BASE_URL}{previous_season}"

#         print("Hey", standings_URL)

#         for team_url in team_urls:
#             team_name = team_url.split(
#                 "/")[-1].replace("-Stats", "").replace("-", " ")

#             data = requests.get(team_url)
#             matches = pd.read_html(data.text, match="Scores & Fixtures")[0]

#             soup = BeautifulSoup(data.text)
#             links = next((a["href"] for a in soup.find_all(
#                 "a") if "all_comps/shooting" in a.get("href", "")), None)

#             data = requests.get(f"{BASE_URL}{links[0]}")
#             shooting = pd.read_html(data.text, match="Shooting")[0]
#             shooting.columns = shooting.columns.droplevel()

#             try:
#                 team_data = matches.merge(
#                     shooting[['Date', 'Sh', 'SoT', 'Dist', 'FK', 'PK', "PKatt"]], on="Date")
#             except ValueError:
#                 continue

#             team_data = team_data[team_data["Comp"] == 'Premier League']
#             team_data['Season'] = year
#             team_data['Team'] = team_name
#             all_matches.append(team_data)
#             time.sleep(1)

#             match_df = pd.concat(all_matches)
#             match_df.columns = [c.lower() for c in match_df.columns]

#             match_df.to_csv("N_matches.csv")


import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

BASE_URL = "https://fbref.com"
PREMIER_LEAGUE_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"
YEARS = list(range(2021, 2020, -1))
SHOOTING_COLUMNS = ['Date', 'Sh', 'SoT', 'Dist', 'FK', 'PK', 'PKatt']

print(YEARS)


def get_team_urls(standings_url):
    try:
        response = requests.get(standings_url)
        if response.status_code == 429:
            print("Too many requests. Waiting and retrying...")
            time.sleep(10)  # Wait for 10 seconds before retrying
            return get_team_urls(standings_url)  # Recursive retry
        response.raise_for_status()
    except RequestException as err:
        raise RuntimeError(f"Error fetching {standings_url}: {err}") from err

    soup = BeautifulSoup(response.content, 'html.parser')
    standings_table = soup.select_one('table.stats_table')
    links = [a['href'] for a in standings_table.select('a[href*="/squad"]')]
    team_urls = [f"{BASE_URL}{link}" for link in links]

    previous_season = soup.select("a.prev")[0].get("href")
    return team_urls, f"{BASE_URL}{previous_season}"


def get_shooting_link(soup):
    link = next((a["href"] for a in soup.find_all(
                 "a") if "all_comps/shooting" in a.get("href", "")), None)

    return f"{BASE_URL}{link}" if link else None


if __name__ == "__main__":
    all_matches = []

    for year in YEARS:
        team_urls, standings_URL = get_team_urls(PREMIER_LEAGUE_URL)
        for team_url in team_urls:
            team_name = team_url.split(
                "/")[-1].replace("-Stats", "").replace("-", " ")

            try:
                data = requests.get(team_url)
                data.raise_for_status()
                matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
                soup = BeautifulSoup(data.text, 'html.parser')
                shooting_link = get_shooting_link(soup)

                if shooting_link:
                    shooting_data = requests.get(shooting_link)
                    shooting = pd.read_html(
                        shooting_data.text, match="Shooting")[0]
                    shooting.columns = shooting.columns.droplevel()

                    team_data = matches.merge(
                        shooting[SHOOTING_COLUMNS], on="Date")
                    team_data = team_data[team_data["Comp"]
                                          == 'Premier League']
                    team_data['Season'] = year
                    team_data['Team'] = team_name
                    all_matches.append(team_data)
                    time.sleep(10)
            except (RequestException, ValueError, IndexError, pd.errors.EmptyDataError) as err:
                print(f"Error processing {team_name} ({year}): {err}")
                continue

    match_df = pd.concat(all_matches)
    match_df.columns = [c.lower() for c in match_df.columns]
    match_df.to_csv("fbref_matches.csv", index=False)
