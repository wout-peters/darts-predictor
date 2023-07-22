from bs4 import BeautifulSoup
import requests

url = 'https://clickondarts.com/Darts/Results/8371/M/PDC-World-Championship-2023'

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

#Retrieve text data from page
text = []
data = soup.select('div[class*="row"]')
for elements in data:
    rowText = elements.text
    if (len(rowText) > 0):
        text.append(rowText)

#Clean data to only end up with dates, matchtypes and match data
index = next((i for i, s in enumerate(text) if 'Finalist:' in s), None)
text = text[index+3:]
index = next((i for i, s in enumerate(text) if 'YearWinnerRunner-Up' in s), None)
text = text[:index-1]

#Method to get a list of match dates
def date(dataList):
    dataList.reverse()
    months = set(['January','February','March','April',
    'May','June','July','August','September',
    'October','November','December'])
    matchDates = []
    prevIndex = 0
    rounds = 1
    for i in range(len(dataList)):
        splitString = dataList[i].split()
        if len(splitString) == 2 or len(splitString) == 1:
            rounds += 1
        if not months.isdisjoint(set(splitString)):
            nMatches = (i - prevIndex - rounds)
            dates = [dataList[i]] * nMatches
            matchDates += dates
            prevIndex = i
            rounds = 1
    matchDates.reverse()
    dataList.reverse()
    return matchDates


dates = date(text)
print(text)
print(dates)

    