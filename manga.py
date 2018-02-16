import requests
from bs4 import BeautifulSoup
import json

class Manga():

    """Simple class that holds basic info about a particular manga."""

    def __init__(self):

        """Initializes the object with basic data."""

        self.USER_AGENT = {
            'User-agent': 
            'Mozilla/5.0 (Windows NT 6.1; \
            Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

        self.r = None
        self.stats = None
        self.soup = None
        self.status_code = 404

        self.title = 'N/A'
        self.title_english = 'N/A'
        self.title_synonyms = 'N/A'
        
        self.score = 'N/A'
        self.scored_by = 0
        self.rank = 0
        self.favorites = 0
        self.volumes = 'Unknown'
        self.chapters = 'Unknown'
        
        self.status = 'Unknown'


    def get_page(self, url):
        self.r = requests.get(url, headers = self.USER_AGENT)
        self.status_code = self.r.status_code

    def get_stats(self):
        # Grab the JSON and make it readable
        self.stats = json.loads(self.r.text)

    # Seems MAL has a different format for obscure mangas,
    # probably their database updates popular ones more often
    # so these less known ones require manual parsing for
    # score and rating count.

    def save_score_and_scored_by(self):
        self.score = self.stats['score']
        self.scored_by = self.stats['scored_by']  

        if self.score is None and self.scored_by is None:
            # Alternative link
            r2 = requests.get(self.stats['link_canonical'], 
                              headers = self.USER_AGENT)

            # Get the HTML and make it soup
            self.soup = BeautifulSoup(r2.text, "html.parser")

            # Get new values
            self.score = (self.soup.find("span", string="Score:").
                          next_sibling.strip())

            self.scored_by = int(self.soup.find(class_="statistics-info info1").
                                 previous_sibling.text.split()[2])
            # A little check
            if self.score != "N/A":
                self.score = float(self.score)

    def save_title_English(self):
        if self.stats['title_english'] is not None:
            self.title_english = (self.stats['title_english'].
                                  replace('&#039;', "'").
                                  replace("&amp;", "&"))
            
    def save_title_synonyms(self):
        if self.stats['title_synonyms'] is not None:
            self.title_synonyms = (self.stats['title_synonyms'].
                                   replace(',', ' |').
                                   replace('&#039;', "'").
                                   replace("&amp;", "&"))

    def save_other_stats(self):
        self.title = self.stats['title']
        self.rank = self.stats['rank']
        self.favorites = self.stats['favorites']
        self.status = self.stats['status']
        self.volumes = self.stats['volumes']
        self.chapters = self.stats['chapters']        

    def printData(self):
        print("Title:", self.title)
        print("English title:", self.title_english)
        print("Synonyms:", self.title_synonyms)
        print("Score:", self.score)
        print("Ratings: {:,}".format(self.scored_by))
        print("Overall ranking: #{:,}".format(self.rank))
        print("Favorites: {:,}".format(self.favorites))
        print("Volumes:", self.volumes)
        print("Chapters:", self.chapters)
        print("Status:", self.status)

# Debugging
#manga = Manga()

#manga.get_page("https://api.jikan.me/manga/104346/stats")

#if manga.status_code == 200:
    #manga.get_stats()
    #manga.save_score_and_scored_by()
    #manga.save_other_stats()

#else:
    #print("404 error")
    #manga.printData()