from manga import *

HEADERS = "Name,English title,Synonyms,Score,Ratings,\
Overall ranking,Favorites,Volumes,Chapters,Status\n"


def print_welcome():
    print("",
          "Welcome to the unique script that makes MyAnimeList more useful!\n",
          "Inspired by Rateyourmusic and their awesome database functionality\n",
          "now you can see useful data about your favorite mangakas' work.\n")


def get_author(author_url):
    return author_url.split("/")[-1].replace("_", " ")


def get_manga_table(author_url):
    # Get webpage
    r = requests.get(author_url)

    # Get the HTML and make it soup
    soup = BeautifulSoup(r.text, "html.parser")

    # Get the content table
    content = soup.find(id="content")

    # Get the table with mangas
    return (content.find(string="Published Manga").parent.
                   next_sibling.find_all("tr"))


def get_manga_list(manga_table, manga_list):
    for i, item in enumerate(manga_table, start=1):
        canonical_link = item.find("a").get("href")
        manga_id = canonical_link.split("/")[-2]
        api_url = "https://api.jikan.me/manga/" + manga_id + "/stats"
        
        print("Processing", i, "out of", len(manga_table), "\n")

        manga = Manga()
        
        manga.get_page(api_url)
        
        if manga.status_code == 200:
            manga.get_stats()
            manga.save_score_and_scored_by()
            manga.save_title_English()
            manga.save_title_synonyms()
            manga.save_other_stats()
            manga_list.append(manga)
        
        else:
            print("Oops! Error trying to get", canonical_link,
                  "Status code", manga.status_code, "\n")

    return manga_list    


def show_options(author, manga_list):
    while True:
        print("",
              "Please note that the sorting options are for testing.\n",
              "It's recommended you just save the results to an Excel file.\n\n",
              "1. Sort by score\n",
              "2. Sort by amount of ratings\n",
              "3. Sort by ranking\n",
              "4. Sort by favorites\n",
              "5. Save to Excel file\n",
              "6. Print mangas\n",
              "7. Exit")
    
        choice = input("\nChoose one: ")
        print()
    
        if choice == "5":
            save_to_excel(author, manga_list, HEADERS)
        
        elif choice == "6":
            print_mangas(manga_list)
            
        elif choice == "7":
            break
    
        else:
            sorter(choice, manga_list)


def sort_by_score(manga_list):
    return manga_list.sort(key=lambda x: x.score, reverse=True)


def sort_by_ratings(manga_list):
    return manga_list.sort(key=lambda x: x.scored_by, reverse=True)


def sort_by_ranking(manga_list):
    return manga_list.sort(key=lambda x: x.rank, reverse=True)


def sort_by_favorites(manga_list):
    return manga_list.sort(key=lambda x: x.favorites, reverse=True)


def print_mangas(manga_list):
    for manga in manga_list:
        manga.printData()
        print()


def save_to_excel(author, manga_list, HEADERS):
    with open(author + ".csv", "w", encoding="utf-8") as file:
        file.write(HEADERS)

        for manga in manga_list:
            try:
                file.write(manga.title.replace(",", "") + "," + 
                           manga.title_english + "," +
                           manga.title_synonyms + "," +
                           str(manga.score) + "," +
                           str(manga.scored_by)  + "," +
                           str(manga.rank)  + "," +
                           str(manga.favorites) + "," +
                           str(manga.volumes).replace("-1", "?") + "," +
                           str(manga.chapters).replace("-1", "?") + "," +
                           manga.status + "\n")
            except:
                pass

        print("\nFinished! Saved as '" + author + ".csv'\n")


def sorter(choice, manga_list):
    if choice == "1":
        sort_by_score(manga_list)

    if choice == "2":
        sort_by_ratings(manga_list)

    if choice == "3":
        sort_by_ranking(manga_list)

    if choice == "4":
        sort_by_favorites(manga_list)

    print("Done!\n")


# Testing
author_url = "https://myanimelist.net/people/2410/Junji_Ito"
author = get_author(author_url)

print_welcome()

manga_table = get_manga_table(author_url)

manga_list = []
manga_list = get_manga_list(manga_table, manga_list)

show_options(author, manga_list)