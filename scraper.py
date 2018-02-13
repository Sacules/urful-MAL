from manga import *

# Testing
mango_list = []
test_list = ["https://myanimelist.net/manga/20375/Black_Paradox",
             "https://myanimelist.net/manga/90477/Ghost_Heights_Kanri_Kumiai",
             "https://myanimelist.net/manga/909/Gyo__Ugomeku_Bukimi",
             "https://myanimelist.net/manga/66425/Kai_Sasu",
             "https://myanimelist.net/manga/82195/Masei",
             "https://myanimelist.net/manga/912/Tomie",
             "https://myanimelist.net/manga/436/Uzumaki"
             ]

for link in test_list:
    mango = Manga(link)
    mango_list.append(mango)

mango_list.sort(key=lambda z: z.score, reverse=True)

for mango in mango_list:
    mango.printData()
    print()
    
