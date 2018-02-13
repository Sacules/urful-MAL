import requests
from bs4 import BeautifulSoup
import time

class Manga():

    """Simple class that holds basic info about a particular manga."""

    def __init__(self, url, name):

        """
        Initializes the object and extracts HTML from the url.

        Args:
            url: MyAnimeList link of the manga's page, must be a string.
        """

        # Get webpage
        r = requests.get(url, headers = {
            'User-agent': 
            'Mozilla/5.0 (Windows NT 6.1; \
            Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'})

        # Get the HTML and make it soup
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Seems MAL has a different format for obscure mangas,
        # probably their database updates popular ones more often
        # so these less known ones require a different technique
        # for score and rating count.
        
        # Get the score
        self.score = soup.find(itemprop="ratingValue")
        
        if self.score is None:
            self.score = float(soup.find("span", string="Score:").
                                   next_sibling.strip())
        else:
            self.score = float(self.score.text)

        # Get the score count
        self.rating_count = soup.find(itemprop="ratingCount")

        if self.rating_count is None:
            self.rating_count = int(soup.find(class_="statistics-info info1").
                                        previous_sibling.text.split()[2])
        
        else:
            self.rating_count = int(self.rating_count.text)
        
        # Set name
        self.name = name
        
        # Get ranked position
        self.ranked = int(soup.find("span", string="Ranked:").
                          next_sibling.replace("#", ""))
        
        # Get amount of favorites
        self.favorites = int(soup.find("span", string="Favorites:").
                             next_sibling.replace(",", ""))


    def printData(self):
        print("Name:", self.name)
        print("Score:", self.score)
        print("Ratings: {:,}".format(self.rating_count))
        print("Overall ranking: #{:,}".format(self.ranked))
        print("Favorites: {:,}".format(self.favorites))




