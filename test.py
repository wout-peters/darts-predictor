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
    numMatches = []
    prevIndex = 0
    rounds = 1
    for i in range(len(dataList)):
        splitString = dataList[i].split()
        if len(splitString) == 2 or len(splitString) == 1:
            rounds += 1
        if not months.isdisjoint(set(splitString)):
            nMatches = (i - prevIndex - rounds)
            dates = [dataList[i]] * nMatches
            numMatches += [nMatches]
            matchDates += dates
            prevIndex = i
            rounds = 1
    matchDates.reverse()
    dataList.reverse()
    numMatches.reverse()
    return matchDates,numMatches

dates,numMatches = date(text)
print(dates)
print(numMatches)
    
def deleteDatesAndRounds(data,dates):
    rounds = ['Final','Semi','Quarter','Round 6','Round 5','Round 4','Round 3','Round 2','Round 1','Qual']
    data = [item for item in data if item not in dates]
    data = [item for item in data if item not in rounds]    
    return data

data = deleteDatesAndRounds(text,dates)
print(data)