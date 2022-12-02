import requests
from bs4 import BeautifulSoup

# URL = "https://www.pro-football-reference.com/years/"
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, "html.parser")

class FantasyScraper:
    base_url = "https://www.pro-football-reference.com/years/"

    def __init__(self, years):
        self.years = years
    
    def print_years(self):
        for year in self.years:
            print(year)

    def scan_matchup(self):
        return 0

    def scan_year(self):
        return 0

def main():
    years = ["2019"]
    scraper = FantasyScraper(years)
    scraper.print_years()

if __name__ == "__main__":
    main()




# results = soup.find(id="wrap")
# job_elements = results.find_all("td", class_="right gamelink")

