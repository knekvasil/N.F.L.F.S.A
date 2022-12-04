import requests
from bs4 import BeautifulSoup

class FantasyScraper:
    base_url = "https://www.pro-football-reference.com/"

    def __init__(self, years):
        self.years = years
            
    def init_soup(self, site_url: str) -> None:
    	if type(site_url) != str:
    		raise TypeError("Params: site_url must be of type str")
    		
    	page = requests.get(site_url)
    	soup = BeautifulSoup(page.content, "html.parser")
    	# Crop page to only include divs with relevant data
    	cropped_page = soup.find(id="content")
    	
    	return cropped_page
    	

    def get_fixture_data(self, fixture_id: str):
    	if type(fixture_id) != str:
    		raise TypeError("Params: fixture_id must be of type str")
    		
    	fixture_url = f"{self.base_url}boxscores/{fixture_id}.htm"
    	page = self.init_soup(fixture_url)
    	
    	# TODO: Grab + store fixture data
    	
    	return page

    
    def get_fixtures_by_week(self, week: str, year: str) -> list:
    	if type(week) != str or type(year) != str:
    		raise TypeError("Params: week, year must be of type str") 
    		
    	week_url = f"{self.base_url}years/{year}/week_{week}.htm"
    	page = self.init_soup(week_url)
    	
    	fixture_summaries = page.find_all("td", class_="right gamelink")
    	
    	fixture_ids = list()
    	for fixture_summary in fixture_summaries:
    		fixture_id = fixture_summary.find("a")
    		fixture_ids.append(fixture_id['href'][11:-4])
    		
    	return fixture_ids


def main():
    years = ["2019"]
    scraper = FantasyScraper(years)
    
    # Testing:
    # print(scraper.get_fixtures_by_week("1", "2019"))
    # print(scraper.get_fixture_data("/boxscores/201909080min.htm"))


if __name__ == "__main__":
    main()


