import bs4
import urllib.request as ur
import re

hdr = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'
}
def re_conv(string):
	return re.sub(r'\'','',string)

def re_modify_wiki(string):
	return re.sub(r'\?object.*','',string) + "/Achievements_and_Trophies"

def check_if_wiki_and_get_href(tag):
	if tag.string == "Wiki":
		return str(tag['href'])

def get_wiki(lst):
	for val in lst:
		if val != None:
			return val

def check_trophy_link(trophy):
	try:
		if(trophy.a):
			return True
	except:
		return False

def filterer(element):
	section,title = element
	sections = section.find_all('a')
	is_exit = False
	for section_type in sections:
		if section_type.string == "Wiki":
			is_exit = True
			break
	if is_exit:
		return True
	return False

def search_game():
	
	game = input("enter the game's name: ")
	game = ur.pathname2url(game)
	search_link = "https://www.ign.com/search?q=" + game + "&page=0&count=15&type=object&filter=games&objectType=game&"
	req=ur.Request(search_link,headers=hdr)
	obj=ur.urlopen(req)
	soup=bs4.BeautifulSoup(obj,features='lxml')
	items_sections = soup.find_all('div', attrs={"class":"sections"})
	items_titles = soup.find_all('div', attrs={"class":"search-item-title"})
	items_sections =  [section for section,title in list(filter(filterer,list(zip(items_sections,items_titles))))]
	items_titles = [title for section,title in list(filter(filterer,list(zip(items_sections,items_titles))))]

	for item,idx in zip(items_titles,list(range(0,len(items_titles)))):
			print(idx," - ",' '.join([re_conv(repr(string)) for string in item.a.stripped_strings]))
	selected_game = input("enter the game: ")

	wiki_link = re_modify_wiki(get_wiki(list(check_if_wiki_and_get_href(anchor) for anchor in items_sections[int(selected_game)].find_all('a'))))
	req=ur.Request(wiki_link,headers=hdr)
	obj=ur.urlopen(req)
	soup=bs4.BeautifulSoup(obj,features='lxml')
	if(soup.find_all('div',attrs={"class":"empty-page"})):
		print("No Trophies")
		return
	
	trophies = soup.find_all('div', attrs={"class":"gh-trophy-title"})
	for trophy in trophies:
		if(check_trophy_link(trophy)):
			print(trophy.a.string + " -- ign.com" + trophy.a["href"])
		else:
			print(trophy.string)

if __name__ == '__main__':
	search_game();