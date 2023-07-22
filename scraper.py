import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

#Use web bot to get links to data pages 
def getLinks(url, years, categories):
    #Initiate browser
    service = ChromeService(executable_path="C:\\Users\\Wout Peters\\webdriver\\chromedriver.exe")
    browser = webdriver.Chrome(service = service)

    dataLinks = []
    browser.get(url)

    browser.delete_all_cookies()

    for year in years:
        try:
            browser.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_cboYear"]/option['+year+']').click()
        except:
            print("year not found")
        finally:
            for cat in categories:
                try:
                    browser.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_cboCategories"]/option['+cat+']').click()
                except:
                    print("category not found")
                finally:
                    div_element = browser.find_elements(By.CSS_SELECTOR, '.row.text-center.ContentLine')
                    for el in div_element:
                        try:
                            link = el.find_element(By.LINK_TEXT, el.text.split('\n')[1])
                        except:
                            pass
                        else:
                            #print(link.text)
                            dataLinks.append(link.get_attribute('href'))
    browser.quit()
    return dataLinks

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
    
#Use web scraper to get dataframe with matches and results
#Perhaps use previous winners?
def getData(URL):
    matches = pd.DataFrame(columns=['year','event','location','date','round','player1','player2','score1','score2'])

    #Initialize web scraper
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    #----------------------------------------------------Does this work?/Do we want to keep it?-------------------------------------
    #Get year of event
    year_element = soup.find(id='mainContentPlaceHolder_cboYear')
    year_selected = year_element.select('[selected]')
    for years in year_selected:
        year = years
    
    #Get event name
    event_element = soup.find(id='mainContentPlaceHolder_cboEvents')
    event_selected = event_element.select('[selected]')
    for events in event_selected:
        event = events
    
    #Get location name
    location = soup.find(id='mainContentPlaceHolder_lblLocation').text

    #-------------------------------------------------------------------------------------------------------------------------------

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

    dates = date(text)
    


def main():
    #Specify subcategories for click instructions.
    #Years: 1 = 2023, 2 = 2022, etc.
    #Categories: 2 = Major events, 3 = European tour, 4 = Players championship
    #5 = World series
    years = ['1','2','3','4','5','6']
    categories = ['2','3','4','5']
    URLs = getLinks('https://clickondarts.com/DartsStats.aspx',years,categories)
    print(URLs)
    #getData(URLs[0]).head()

if __name__ == "__main__":
    main()
