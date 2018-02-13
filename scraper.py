from manga import *
import time

author_url = "https://myanimelist.net/people/2410/Junji_Ito"

# Get webpage
r = requests.get(author_url)

# Get the HTML and make it soup
soup = BeautifulSoup(r.text, "html.parser")

# Get the content table
content = soup.find(id="content")

# Get the table with mangas
manga_list = (content.find(string="Published Manga").parent.next_sibling.
              find_all("tr"))

mango_list = []
counter = 1

for manga in manga_list:
    name = manga.contents[3].a.text
    link = manga.find("a").get("href")
        
    mango = Manga(link, name)

    print("\nProcessing", counter, "out of", len(manga_list), "\n")
    counter += 1
    
    mango_list.append(mango)
    mango.printData()
