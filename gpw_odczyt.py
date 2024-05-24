import requests
from bs4 import BeautifulSoup

asset_list = [
	"https://www.gpw.pl/spolka?isin=PLPKN0000018",  # orlen
	"https://www.gpw.pl/spolka?isin=PLOPTTC00011",  # cd projekt
	"https://www.gpw.pl/spolka?isin=PLGPW0000017",  # gpw
	"https://www.gpw.pl/spolka?isin=PLBH00000012",  # handlowy
	"https://www.gpw.pl/spolka?isin=PLMOBRK00013",  # mobruk
]

etf_list = [
	"https://www.gpw.pl/etf?isin=LU0496786574",  # ETFSP500
]


def check_for_values_assets(soup):
	"""
	Picking values from html
	:param soup: response html site from GPW site parsed in BeautifulSoup
	:return: name of asset, current price, current date (and time if available)
	"""
	name = soup.find("small", id="getH1").text.strip()
	price = soup.find("span", class_="summary").text.replace(",", ".")
	current_time = soup.find("div", class_="currentTimeMin").text[-16:]

	return name, price, current_time


def check_for_values_etf(soup):
	"""
	Picking values from html
	:param soup: response html site from GPW site parsed in BeautifulSoup
	:return: name of asset, current price, current date (and time if available)
	"""
	name = soup.find("div", id="nazwa-instrumentu-div").text.strip()
	price = soup.find("span", class_="summary").text.replace(",", ".").strip()
	current_time = soup.find("span", class_="date font12").text

	return name, price, current_time


def check_list(item_list):
	"""
	Checking in loop for specified assets to be scraped for name, price and time of asset
	:param item_list: list of links
	:return:
	"""
	for gpw_item in item_list:
		try:
			response = requests.get(gpw_item)
		except Exception as e:
			print(f"Connection problem, error {e}")

		soup = BeautifulSoup(response.content, 'html.parser')

		if item_list == asset_list:
			name, price, current_time = check_for_values_assets(soup)
		else:
			name, price, current_time = check_for_values_etf(soup)

		file = open(name, "a")
		file.writelines(f"\n{price}, {current_time}")
		file.close()

		print(f"{name}, {price}, {current_time}")


check_list(asset_list)
check_list(etf_list)
