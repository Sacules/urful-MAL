import requests
from bs4 import BeautifulSoup

class Manga():
    
    """Simple class that holds basic info about a particular manga."""
    
    def __init__(self, url):
        
        """
        Initializes the object and extracts HTML from the url.
        
        Args:
            url: MyAnimeList link of the manga's page, must be a string.
        """
        
        # Get webpage
        r = requests.get(url)
        
        # Get the HTML and make it soup
        soup = BeautifulSoup(r.text, "html.parser")

        # information = soup.find_all(class_="js-scrollfix-bottom")
        # To reconsider if performance slows down.
        
        # Get the info
        try:
            self.name = soup.find("span", string="English:").next_sibling.strip()
        
        # Some mangas don't have an official English title
        except:
            self.name = soup.find("span", string="Japanese:").next_sibling.strip()
        
        finally:
            self.score = float(soup.find(itemprop="ratingValue").text)
            self.rating_count = int(soup.find(itemprop="ratingCount").text)
            self.ranked = int(soup.find("span", string="Ranked:").
                         next_sibling.replace("#", ""))
            self.favorites = int(soup.find("span", string="Favorites:").
                             next_sibling.replace(",", ""))


    def printData(self):
        print("Name:", self.name)
        print("Score:", self.score)
        print("Ratings: {:,}".format(self.rating_count))
        print("Overall ranking: #{:,}".format(self.ranked))
        print("Favorites: {:,}".format(self.favorites))
