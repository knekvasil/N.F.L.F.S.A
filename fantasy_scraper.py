import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import json

class FantasyScraper:
    base_url = "https://www.pro-football-reference.com/"

    def __init__(self, years):
        self.years = years
            
    # Initialize scraper on given site url
    def init_soup(self, site_path: str) -> "bs4.element.Tag":
    	response = requests.get(site_path)
    	soup = BeautifulSoup(response.content, "html.parser")
    	# Crop page to only include divs with relevant data (ignore header, footer, etc.)
    	cropped_page = soup.find(id="content")
    	
    	return cropped_page
    	

    def get_fixture_data(self, fixture_id: str) -> dict:
    	fixture_url = f"{self.base_url}boxscores/{fixture_id}.htm"
    	cropped_page = self.init_soup(fixture_url)
    	
    	# The only relevant table that can be found without sorting through commented fragments (old version)
    	self.get_passing_rushing_receiving(cropped_page)
    	
    	# Grab all other tables on page (new version)
    	# Old version for getting tables failed because many tables are commented out
    	fixture_table_fragments = cropped_page.find_all(string=lambda text: isinstance(text, Comment))
    	
    	table_fragments = list()
  
    	for table_fragment in fixture_table_fragments:
    		if "table" in table_fragment:
    			try:
    				table_fragments.append(table_fragment)
    			except:
    				continue	
    	
    	# Filter out non-relevant tables
    	filter_indices = [5,6,7,8,9,10,11,14,15,16,18]
    	filtered_tables = [table_fragments[i] for i in filter_indices]
    	
    	# Testing
    	# for t in filtered_tables:
    	# 	print(pd.read_html(t))
    	
    	# Todo: compartmentalize + eval each table like get_passing_rushing_receiving()
    	
    	return 0
		
    
    # Grab all fixture links from weekly matchup page
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
    	
    
    # Get offense player stats (Generic)
    def get_passing_rushing_receiving(self, cropped_page: "bs4.element.Tag") -> dict:   
    	# Get p,r,r stats 	
    	off_player_table = cropped_page.find(id="all_player_offense")
    	off_player_table_body = off_player_table.find("tbody")
    	
    	off_player_store = dict()
    	# Loop through player rows
    	for row in off_player_table_body.findAll("tr"):
    		# Filter out non-player rows
    		player_name_row = row.find("a")
    		if player_name_row:
    			# Init player store dict
    			player_name = player_name_row.get_text()
    			off_player_store[player_name] = dict()
    			# Manually looping though columns simplifies stat retrieval 
    			for col in row.findAll("td"):
    				off_player_store[player_name][col["data-stat"]] = col.get_text()
		# Testing
    	print(json.dumps(off_player_store, indent=2))
  
    	return off_player_store
    	
    
    # Get kicker player stats
    def get_kicking(self, cropped_page: "bs4.element.Tag") -> dict:
    	return 0
    
    
    # Get returns player stats
    def get_returns(self, cropped_page: "bs4.element.Tag") -> dict:
    	return 0
    	
    	
    # A lot of required player data is not given upfront.
    # The simplest solution is to loop through the play-by-play feed and look for cases manually
    # This could get ugly...
    def get_play_by_play(self, cropped_page: "bs4.element.Tag") -> dict:
    	return 0;
    	
    
    def parse_table_data(self, table_element: "bs4.element.Tag") -> dict:
    	return 0;
    	
    
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

