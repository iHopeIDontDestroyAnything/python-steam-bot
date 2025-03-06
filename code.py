import func 
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


url1 = "https://steamcommunity.com/market/listings/730/M249%20%7C%20Hypnosis%20%28Field-Tested%29"
url2 = "https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20Sawed-Off%20%7C%20Black%20Sand%20%28Field-Tested%29"    


urlList = [url1,url2]

options = Options() 
options.add_extension("/home/jakub/venv/cs_float.crx")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options = options)

func.loadCookies(driver,url1)
#func.newCookies(driver,url1,50)

#need delay for the site to load propertly
func.printListings(driver,urlList)

driver.quit()
