from manga import *

HEADERS = "Name,Score,Ratings,Overall ranking,Favorites\n"


def get_author(author_url):
    return author_url.split("/")[-1].replace("_", " ")


def get_mangas(author_url):
    # Get webpage
    r = requests.get(author_url)
    
    # Get the HTML and make it soup
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Get the content table
    content = soup.find(id="content")
    
    # Get the table with mangas
    manga_table = (content.find(string="Published Manga").parent.
                   next_sibling.find_all("tr"))
    
    # Initialize
    manga_list = []

    # Add mangas to list
    for i, item in enumerate(manga_table, start=1):
        name = item.contents[3].a.text
        link = item.find("a").get("href")
        
        print("Processing", i, "out of", len(manga_table), "\n")
        
        manga = Manga(link, name)

        manga_list.append(manga)
    
    return manga_list


def sort_by_score(manga_list):
    return manga_list.sort(key=lambda x: x.score, reverse=True)


def sort_by_ratings(manga_list):
    return manga_list.sort(key=lambda x: x.rating_count, reverse=True)


def sort_by_ranking(manga_list):
    return manga_list.sort(key=lambda x: x.ranked, reverse=True)


def sort_by_favorites(manga_list):
    return manga_list.sort(key=lambda x: x.favorites, reverse=True)


def print_mangas(manga_list):
    for manga in manga_list:
        manga.printData()
        print("")


def save_to_excel(author, manga_list, HEADERS):
    with open(author + ".csv", "w", encoding="utf-8") as file:
        file.write(HEADERS)

        for manga in manga_list:
            file.write(manga.name + "," + 
                       str(manga.score) + "," +
                       str(manga.rating_count)  + "," +
                       str(manga.ranked)  + "," +
                       str(manga.favorites) + "\n")

        print("Finished! Saved as", author, ".csv")


def sorter(author, choice, manga_list):
    if choice == "1":
        sort_by_score(manga_list)

    if choice == "2":
        sort_by_ratings(manga_list)

    if choice == "3":
        sort_by_ranking(manga_list)

    if choice == "4":
        sort_by_favorites(manga_list)

    if choice == "5":
        save_to_excel(author, manga_list, HEADERS)

    if choice == "6":
        pass


# Testing
author_url = "https://myanimelist.net/people/4580/Satoshi_Kon"
author = get_author(author_url)
manga_list = get_mangas(author_url)

print_mangas(manga_list)

while True:
	print("",
     	 "1. Sort by score\n",
     	 "2. Sort by amount of ratings\n",
	 "3. Sort by ranking\n",
     	 "4. Sort by favorites\n",
     	 "5. Save to Excel file\n",
     	 "6. Exit")

	choice = input("\nChoose one: ")
	print()

	if choice == "6":
	    break

	sorter(author, choice, manga_list)

	print_mangas(manga_list)
