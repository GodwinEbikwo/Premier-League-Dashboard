import asyncio
import logging
import time

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

logger = logging.getLogger('scraper')

BASE_URL = "https://fbref.com"
PREMIER_LEAGUE_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"
YEARS = list(range(2022, 2020, -1))
SHOOTING_COLUMNS = ['Date', 'Sh', 'SoT', 'Dist', 'FK', 'PK', 'PKatt']


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def get_shooting_link(soup):
    link = next((a["href"] for a in soup.find_all("a")
                if "all_comps/shooting" in a.get("href", "")), None)
    return f"{BASE_URL}{link}" if link else None


async def get_team_data(session, team_url):
    html = await fetch(session, team_url)
    soup = BeautifulSoup(html, 'html.parser')

    matches = pd.read_html(html, match="Scores & Fixtures")[0]
    shooting_link = get_shooting_link(soup)

    if not shooting_link:
        logger.warning(f"No shooting data for {team_url}")
        return None

    shooting_html = await fetch(session, shooting_link)
    shooting = pd.read_html(shooting_html, match="Shooting")[0]
    shooting.columns = shooting.columns.droplevel()

    team_data = matches.merge(shooting[SHOOTING_COLUMNS], on="Date")
    team_data = team_data[team_data["Comp"] == 'Premier League']

    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
    team_data['Team'] = team_name

    return team_data


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        all_data = []

        for year in YEARS:
            standings_url = PREMIER_LEAGUE_URL
            team_urls, prev_url = await get_team_data(session, standings_url)

            for team_url in team_urls:
                task = asyncio.create_task(get_team_data(session, team_url))
                tasks.append(task)

            PREMIER_LEAGUE_URL = prev_url

            team_data = await asyncio.gather(*tasks)
            all_data.extend(d for d in team_data if d is not None)
            time.sleep(10)

        df = pd.concat(all_data)
        df.to_csv("premier_league.csv", index=False)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
