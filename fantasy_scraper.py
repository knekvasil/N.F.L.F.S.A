import requests
from bs4 import BeautifulSoup
import json

class FantasyScraper:
    base_url = "https://www.pro-football-reference.com/"

    def __init__(self, years):
        self.years = years
            
    def init_soup(self, site_url: str) -> "bs4.element.Tag":
    	page = requests.get(site_url)
    	soup = BeautifulSoup(page.content, "html.parser")
    	# Crop page to only include divs with relevant data
    	cropped_page = soup.find(id="content")
    	
    	return cropped_page
    	

    def get_fixture_data(self, fixture_id: str):
    	fixture_url = f"{self.base_url}boxscores/{fixture_id}.htm"
    	cropped_page = self.init_soup(fixture_url)
    	
    	offense_stats = self.get_passing_rushing_receiving(cropped_page)
    	
    	# Todo:
    	# - Defense (+ Special Teams)
    	# - Kicking

    	return cropped_page

    
    def get_fixtures_by_week(self, week: str, year: str) -> list:
    	week_url = f"{self.base_url}years/{year}/week_{week}.htm"
    	cropped_page = self.init_soup(week_url)
    	
    	# Get fixture list
    	fixture_summaries = cropped_page.find_all("td", class_="right gamelink")
    	
    	fixture_ids = list()
    	for fixture_summary in fixture_summaries:
    		fixture_id = fixture_summary.find("a")
    		fixture_ids.append(fixture_id['href'][11:-4])
    		
    	return fixture_ids
    
    # Get offense player stats
    def get_passing_rushing_receiving(self, cropped_page):
    	player_store = dict()
    	
    	off_player_table = cropped_page.find(id="player_offense")
    	off_player_table_body = off_player_table.find("tbody")
    	
    	off_players = dict()
    	# Loop through player rows
    	for row in off_player_table_body.findAll("tr"):
    		# Filter out non-player rows
    		player_name_row = row.find("a")
    		if player_name_row:
    			# Init player store dict
    			player_name = player_name_row.get_text()
    			off_players[player_name] = dict()
    			# Manually looping though columns simplifies stat retrieval 
    			for col in row.findAll("td"):
    				off_players[player_name][col["data-stat"]] = col.get_text()
		# Testing
    	# print(json.dumps(off_players, indent=2))
  
    	return off_players


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

