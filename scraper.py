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

    for year in years:
        browser.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_cboYear"]/option['+year+']').click()
        for cat in categories:
            browser.find_element(By.XPATH, '//*[@id="mainContentPlaceHolder_cboCategories"]/option['+cat+']').click()
            div_element = browser.find_elements(By.CSS_SELECTOR, '.row.text-center.ContentLine')
            for el in div_element:
                try:
                    link = el.find_element(By.LINK_TEXT, el.text.split('\n')[1])
                except:
                    pass
                else:
                    print(link.text)
                    dataLinks.append(link.get_attribute('href'))
    browser.quit()
    return dataLinks


#Use web scraper to get dataframe with matches and results
#Perhaps use 
matches = pd.DataFrame(columns=['year','event','location','date','round','player1','player2','score1','score2'])

for URL in dataLinks:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    year_element = soup.select_one('select[name="ctl00$mainContentPlaceHolder$cboYear"]')
    year = year_element.get('value')
    print(year)


def main():
    #Specify subcategories for click instructions.
    #Years: 1 = 2023, 2 = 2022, etc.
    #Categories: 2 = Major events, 3 = European tour, 4 = Players championship
    #4 = World series
    years = ['1','2','3','4','5','6']
    categories = ['2','3','4','5']
    URLs = getLinks('https://clickondarts.com/DartsStats.aspx',years,categories)


if __name__ == "__main__":
    main()
