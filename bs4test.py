from bs4 import BeautifulSoup, SoupStrainer
import requests
import cProfile
import pstats

r = requests.get("https://www.basketball-reference.com/leagues/NBA_2022_per_game.html").text
s = SoupStrainer("a")
print(BeautifulSoup(r,"html5lib", parse_only= SoupStrainer).prettify())
# t_data = BeautifulSoup(r,"html5lib").find("table").tbody.find_all("tr")

# data = {}
# for row in t_data:
#     td = row.find_all("td")
#     try:
#       data[td[0].text] = float(td[-1].text)
#     except IndexError:
#       pass

# print(sorted(data.items(), key = lambda x: -x[1]))

# for td in t_data[0].find_all("td"):
#   print(td.text)

# cProfile.run('main()','data')
# p = pstats.Stats('data')
# p.strip_dirs().sort_stats('time').print_stats(20)