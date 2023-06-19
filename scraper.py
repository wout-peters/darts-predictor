import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

#Initiate browser
service = ChromeService(executable_path="C:\\Users\\Wout Peters\\webdriver\\chromedriver.exe")
browser = webdriver.Chrome(service = service)
#browser.get('https://www.instagram.com/')




browser.quit()

#URL = "https://clickondarts.com/DartsStats.aspx"
#page = requests.get(URL)
#print(page.text)