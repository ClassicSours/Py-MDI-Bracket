import requests
from bs4 import BeautifulSoup
from selenium import webdriver


url = 'https://raider.io/mythic-dungeon-international/spring-2019-time-trials/west-1/'

web_r = requests.get(url)
web_soup = BeautifulSoup(web_r.text,'html.parser')

driver = webdriver.Firefox(executable_path=r'/usr/bin/firefox')
driver.get(url)
html = driver.execute_script("return document.documentElement.outerHTML")

sel_soup = BeautifulSoup(html,'html.parser')
print(sel_soup.text)
