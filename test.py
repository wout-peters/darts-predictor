from bs4 import BeautifulSoup
import requests

url = 'https://clickondarts.com/Darts/Results/8371/M/PDC-World-Championship-2023'

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
year_element = soup.find(id='mainContentPlaceHolder_cboYear')
year_selected = year_element.select('[selected]')
for year in year_selected:
    print(year.text)

#year_selected = year_element.select('option[selected]')
#print(year_selected)
#year = year_selected.get('value')
#print(year)