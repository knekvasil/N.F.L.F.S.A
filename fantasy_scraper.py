import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup, Comment
import json
from mergedeep import merge


class FantasyScraper:
    base_url = "https://www.pro-football-reference.com/"

    def __init__(self, years):
        self.years = years

    # Initialize scraper on given site url
    def init_soup(self, site_path: str) -> bs4.element.Tag:
        response = requests.get(site_path)
        soup = BeautifulSoup(response.content, "html.parser")
        # Crop page to only include divs with relevant data (ignore header, footer, etc.)
        cropped_page = soup.find(id="content")

        return cropped_page

    # Grab and filter all relevant matchup data
    def get_fixture_data(self, fixture_id: str) -> dict:
        fixture_url = f"{self.base_url}boxscores/{fixture_id}.htm"

        cropped_page = self.init_soup(fixture_url)

        # The page renders tables as either Tags or Comments. In our case, the only Tag
        # table we care about is the all_player_offense table
        off_player_table = cropped_page.find(id="all_player_offense")
        off_player_table_body = off_player_table.find("tbody")

        # Grab all Comments on page
        fixture_table_fragments = cropped_page.find_all(
            string=lambda text: isinstance(text, Comment))

        table_fragments = list()

        # Filter out non-table comments
        for table_fragment in fixture_table_fragments:
            if "table" in table_fragment:
                try:
                    table_fragments.append(table_fragment)
                except:
                    continue

        # Filter out non-relevant tables (PBP can be parsed but it makes life more difficult)
        # Two tables require unique parsing: team_stats and play-by-play
        # table_fragments[4] = team_stats (Tag: wherever)
        # table_fragments[18] = play-by-play (Comment: post-table_fragments)
        filter_indices = [5, 6, 7, 8, 9, 10, 11, 14, 15, 16]

        # Insert Tag table grabbed earlier to filtered table fragments list
        filtered_tables = [off_player_table_body] + [table_fragments[i] for i in filter_indices]

        player_stats_store = dict()

        # Get data from generic tables
        for table_fragment in filtered_tables:
            table_data = self.get_table_data(table_fragment)
            # Merging dicts with embedded keys is not trivial. Let a package do it for us instead
            merge(player_stats_store, table_data)

        # Get data from non-generic tables (different table formatting)
        # play-by-play table
        pbp_store = self.get_pbp_table_data(table_fragments[18])
        # team stats table
        team_stats_store = self.get_team_stats_table_data(table_fragments[4])

        # Debugging
        # print(json.dumps(player_stats_store, indent=2))
        # print(json.dumps(pbp_store, indent=2))
        # print(json.dumps(team_stats_store, indent=2))

        return 0

    # Grab all fixture links from weekly matchup page
    def get_fixtures_by_week(self, week: str, year: str) -> list:
        week_url = f"{self.base_url}years/{year}/week_{week}.htm"
        cropped_page = self.init_soup(week_url)

        # Get fixture list
        fixture_summaries = cropped_page.find_all(
            "td", class_="right gamelink")

        fixture_ids = list()
        for fixture_summary in fixture_summaries:
            fixture_id = fixture_summary.find("a")
            fixture_ids.append(fixture_id['href'][11:-4])

        return fixture_ids

    # Get all player stats by grouping
    def get_table_data(self, table_fragment: bs4.element) -> dict:
        if type(table_fragment).__name__ == "Comment":
            # Parse Comment back into Tag
            table_soup = BeautifulSoup(table_fragment, "html.parser")
            player_table_rows = table_soup.find_all("tr")
        else:
            # table_fragment is a Tag
            player_table_rows = table_fragment.find_all("tr")

        player_store = dict()

        for row in player_table_rows:
            player_name_row = row.find("a")
            if player_name_row:
                player_name = player_name_row.get_text()
                player_uid = player_name_row["href"].rsplit("/", 1)[-1]
                # init unique identifier (<a> tag url link) in case of unique names
                player_store[player_uid] = {"name": player_name}

                for col in row.find_all("td"):
                    player_store[player_uid][col["data-stat"]] = col.get_text()

        return player_store

    # Due to the structure of the table, a different parsing appreach is required
    # Try to modularize with get_table_data() after if possible
    def get_team_stats_table_data(self, team_stats_table_fragment: bs4.element.Comment) -> dict:
        ts_table_soup = BeautifulSoup(team_stats_table_fragment, "html.parser")
        team_stats = ts_table_soup.find_all("tr")

        ts_store = {"home_stat": {}, "vis_stat": {}}

        teams = team_stats[0].find_all("th")
        for team in teams:
            if team["data-stat"] != "stat":
                ts_store[team["data-stat"]] = {"name": team.get_text()}

        for row in team_stats:
            header = row.find("th")
            if header.get_text() != "":
                data = row.find_all("td")
                for datum in data:
                    ts_store[datum["data-stat"]][header.get_text()] = datum.get_text()

        return ts_store

    # Custom function required
    # Searching by HTML tag <a> seems a lot simpler/faster than regex searching through strings...
    def get_pbp_table_data(self, pbp_table_fragment: bs4.element.Comment) -> list:
        pbp_table_soup = BeautifulSoup(pbp_table_fragment, "html.parser")
        pbp_table_rows = pbp_table_soup.find_all("tr")
        # Order matters. "Josh Allen (BUF) sacked by Josh Allen (JAX)." kills dict() storing
        play_store = list()

        for row in pbp_table_rows:
            play_detail = row.find("td", {"data-stat": "detail"})
            if type(play_detail).__name__ != "NoneType" and play_detail.find("a"):
                play_data = {"detail": play_detail.get_text(), "players": []}
                players_involved = play_detail.find_all("a", href=True)
                for player in players_involved:
                    play_data["players"].append((player["href"].rsplit("/", 1)[-1], player.get_text()))

                play_store.append(play_data)

        return play_store


def main():
    years = ["2019"]
    scraper = FantasyScraper(years)

    # Testing:
    # Get all fixture ids for Week 1, 2019 (Functioning)
    # print(scraper.get_fixtures_by_week("1", "2019"))

    # Get game data for GNB v. CHI, Week 1, 2019
    scraper.get_fixture_data("201909080min")


if __name__ == "__main__":
    main()
