# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# import time
# from requests.exceptions import RequestException

# BASE_URL = "https://fbref.com"
# years = list(range(2022, 2016, -1))

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


# def get_player_image_url(player_url):
#     try:
#         response = requests.get(player_url, headers=headers)
#         response.raise_for_status()
#     except RequestException as err:
#         raise RuntimeError(f"Error fetching {player_url}: {err}") from err

#     soup = BeautifulSoup(response.content, "html.parser")
#     media_item_div = soup.find('div', class_='media-item')
#     if media_item_div:
#         img_tag = media_item_div.find('img')
#         if img_tag:
#             image_url = img_tag.get('src')
#             return image_url
#     return None


# if __name__ == "__main__":
#     all_player_data = []

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

#                 soup = BeautifulSoup(team_data.text, 'html.parser')
#                 table_body = soup.find('table', {'id': 'stats_standard_9'})

#                 player_links = table_body.find_all('th', class_='left')

#                 for link in player_links:
#                     player_a_tag = link.find('a')
#                     if player_a_tag:
#                         player_url = BASE_URL + player_a_tag['href']
#                         player_image_url = get_player_image_url(player_url)
#                         player_name = player_a_tag.text
#                         # print(
#                         #     f"Player: {player_a_tag.text}, Image URL: {player_image_url}")

#                         all_player_data.append(
#                             {'player': player_name, 'img_uRL': player_image_url})

#                     time.sleep(5)

#             except (RequestException, ValueError, IndexError, pd.errors.EmptyDataError) as err:
#                 print(f"Error processing {team_name} ({year}): {err}")
#                 continue
#     player_df = pd.DataFrame(all_player_data)
#     player_df.to_csv("player_images.csv", index=False)


import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import concurrent.futures  # For parallel processing
import time

BASE_URL = "https://fbref.com"
years = list(range(2022, 2016, -1))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


def get_team_urls(base_url):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        standings_table = soup.select_one('table.stats_table')
        links = [a['href']
                 for a in standings_table.select('a[href*="/squad"]')]
        team_urls = [f"{BASE_URL}{link}" for link in links]
        return team_urls
    except RequestException as err:
        raise RuntimeError(
            f"Error occurred when fetching {base_url}: {err}") from err


def get_player_image_url(player_url):
    try:
        response = requests.get(player_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        media_item_div = soup.find('div', class_='media-item')
        if media_item_div:
            img_tag = media_item_div.find('img')
            if img_tag:
                image_url = img_tag.get('src')
                return image_url
    except RequestException as err:
        print(f"Error fetching {player_url}: {err}")
    return None


def process_team(team_url):
    try:
        team_data = requests.get(team_url)
        team_data.raise_for_status()
        soup = BeautifulSoup(team_data.text, 'html.parser')
        table_body = soup.find('table', {'id': 'stats_standard_9'})
        player_links = table_body.find_all('th', class_='left')

        player_data = []
        for link in player_links:
            player_a_tag = link.find('a')
            if player_a_tag:
                player_url = BASE_URL + player_a_tag['href']
                player_image_url = get_player_image_url(player_url)
                player_name = player_a_tag.text
                player_data.append(
                    {'player': player_name, 'img_url': player_image_url})
                time.sleep(2)

        return player_data
    except (RequestException, ValueError, IndexError, pd.errors.EmptyDataError) as err:
        print(f"Error processing {team_url}: {err}")
        return []


if __name__ == "__main__":
    all_player_data = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for year in years:
            team_urls = get_team_urls(
                BASE_URL + f"/en/comps/9/{year}-{year+1}/{year}-{year+1}-Premier-League-Stats")
            for team_url in team_urls:
                print(team_url)
                player_data = process_team(team_url)
                all_player_data.extend(player_data)

    player_df = pd.DataFrame(all_player_data)
    player_df.to_csv("player_images_data.csv", index=False)
