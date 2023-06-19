from bs4 import BeautifulSoup
import requests

url = 'https://clickondarts.com/Darts/Results/8371/M/PDC-World-Championship-2023'

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

text = []
data = soup.select('div[class*="row"]')
for elements in data:
    rowText = elements.text
    if (len(rowText) > 0):
        text.append(rowText)

index = next((i for i, s in enumerate(text) if 'Finalist:' in s), None)
text = text[index+3:]

index = next((i for i, s in enumerate(text) if 'YearWinnerRunner-Up' in s), None)
text = text[:index-1]

print(text)
#for elements in dates_elements:
#    dates_selected = elements.select("span[id*=lblFixtureDate_]")
#    for dates in dates_selected:
#        #dateList.append(dates.text)
#        dateMatches.append(dates['id'].split('_')[-1] + 1)

    