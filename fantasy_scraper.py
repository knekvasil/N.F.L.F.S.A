import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
import json

class FantasyScraper:
    base_url = "https://www.pro-football-reference.com/"

    def __init__(self, years):
        self.years = years
            
    def init_soup(self, site_url: str) -> "bs4.element.Tag":
		#headers = {
		#	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:83.0) Gecko/20100101 Firefox/83.0",
		#	"Authorization": "Bearer 2381c6b987aea877abc6a73fe1cbc7d4a88a602c",
		#}

    	page = requests.get(site_url)
    	soup = BeautifulSoup(page.content, "html.parser")
    	# Crop page to only include divs with relevant data
    	cropped_page = soup.find(id="content")
    	
    	return soup
    	

    def get_fixture_data(self, fixture_id: str) -> dict:
    	fixture_url = f"{self.base_url}boxscores/{fixture_id}.htm"
    	cropped_page = self.init_soup(fixture_url)
    	
    	tables = cropped_page.find_all("div", class_="table_wrapper")
    	for table in tables:
    		tabs = table.find_all("div")
    		print(tabs)
    	
    	# offense_stats = self.get_passing_rushing_receiving(cropped_page)
    	# kicking_stats = self.get_kicking(cropped_page)
    	# Todo:
    	# - Defense (+ Special Teams)
    	# - Kicking
    	# print(cropped_page.get_text())
 
    	#tables = self.get_tables(cropped_page)
    	
    	# Nothing Found
    	
    	# tables = cropped_page.findAll("div")
    	# for table in tables:
    		# print(table.get_text())
    	
    	return 0 # cropped_page

    
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
    	
    
    # Get kicker player stats (Generic)
    def get_kicking(self, cropped_page: "bs4.element.Tag") -> dict:
    	kicking_player_table = cropped_page.find(id="kicking")
    	print(kicking_player_table)
    	kicking_player_table_body = kicking_player_table.find("tbody")
    	
    	kicker_store = dict()
    	
    	for row in kicking_player_table_body:
    		player_name_row = row.find("a")
    		if player_name_row:
    			player_name = player_name_row.get_text()
    			kicker_store[player_name] = dict()
    			for col in row.findAll("td"):
    				kicker_store[player_name][col["data-stat"]] = col.get_text()
    	
    	print(json.dumps(kicker_store, indent=2))
    			
    	return kicker_store
    
    
    # Get returns player stats (Generic)
    def get_returns(self, cropped_page: "bs4.element.Tag") -> dict:
    	returns_player_table = cropped_page.find(id="returns")
    	returns_player_table_body = returns_player_table.find("tbody")
    	
    	returner_store = dict()
    	return 0
    	
    	
    # A lot of required player data is not given upfront.
    # The simplest solution is to loop through the play-by-play feed and look for cases manually
    # This could get messy...
    def get_play_by_play(self, cropped_page: "bs4.element.Tag") -> dict:
    	return 0;
    	
    
    def parse_table_data(self, table_element: "bs4.element.Tag") -> dict:
    	
    	
    	print(table.get_text())
    	return 0;
    	
    


def main():
    #years = ["2019"]
    #scraper = FantasyScraper(years)
    
    # Testing:
    # Get all fixture ids for Week 1, 2019 (Functioning)
    # print(scraper.get_fixtures_by_week("1", "2019"))
    
    # Get game data for GNB v. CHI, Week 1, 2019
    # scraper.get_fixture_data("201909080min")
    
    
    
    
	response = requests.get("https://www.pro-football-reference.com/boxscores/201909080min.htm")

	soup = BeautifulSoup(response.text, 'html.parser')
	comments = soup.find_all(string=lambda text: isinstance(text, Comment))

	tables = []
	for each in comments:
		if 'table' in each:
		    try:
		    	tables.append(each)
		        #tables.append(pd.read_html(each)[0])
		    except:
		        continue

	for table in tables:
		print(table)

    
    # df = pd.read_html(url)[2]
    # print(df.to_string())
    #response = requests.get(url)
    #soup = BeautifulSoup(response.content, "html.parser")
    # p_r = requests.get(url).text
    #tables = soup.find_all("table", text=True)
    #print(tables)
   
   
    # print(json.dumps(data, indent=4))
    


if __name__ == "__main__":
    main()

