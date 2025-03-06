from time import sleep
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

def get_shadow_root(driver,element):
    return driver.execute_script('return arguments[0].shadowRoot', element)

def getFloat(driver, element):
    csfloat_wrapper = element.find_element(By.CSS_SELECTOR,"csfloat-item-row-wrapper")
    float_row = get_shadow_root(driver,csfloat_wrapper).find_element(By.CSS_SELECTOR,"csfloat-float-bar")
    value = float(float_row.get_attribute('float'))
    return value
    #this absolute mess is maybe not necessary but i works :)
    #returns float of a skin in the current listing

def getName(driver, element):
    name = element.find_element(By.CLASS_NAME,"market_listing_item_name").text
    return name

def getLargeListing(driver):
    belt = driver.find_element(By.CSS_SELECTOR,"csfloat-utility-belt")
    getQuantity = get_shadow_root(driver,belt).find_element(By.CSS_SELECTOR,"csfloat-page-size.page-selector")
    _select = get_shadow_root(driver, getQuantity).find_element(By.CSS_SELECTOR,"select")
    select = Select(_select)
    select.select_by_value('100')
    

def sortFloat(driver):
    #csfloat button finding, happy it works
    belt = driver.find_element(By.CSS_SELECTOR,"csfloat-utility-belt")
    sortListings = get_shadow_root(driver,belt).find_element(By.CSS_SELECTOR,"csfloat-sort-listings") 
    preButton = get_shadow_root(driver, sortListings).find_element(By.CSS_SELECTOR,"csfloat-steam-button")
    Button = get_shadow_root(driver,preButton).find_element(By.CLASS_NAME,"btn_small").click()
    #this took longer than i would like to admit

def getPrice(driver,  element):
    value = element.find_element(By.CSS_SELECTOR,"span.market_listing_price.market_listing_price_with_fee").text
    price = []
    for char in value:
        if char.isdigit():
            price.append(char)
        elif char == ',':
            price.append('.')
    price = "".join(price)
    price = float(price)
    return price


def loadCookies(driver,url):
    driver.get(url)
    cookies = pickle.load(open("cookies.pkl","rb")) 
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

 
def newCookies(driver,url,_time):
    time = _time
    driver.get(url)
    i = 0
    while i < time:
        print(time - i)
        i = i + 1
        sleep(1)
    open("cookies.pkl","w").close()
    pickle.dump(driver.get_cookies(),open("cookies.pkl", "wb"))
    print("Reloading")
    loadCookies(driver,url)

def printListings(driver,urlList):
    for url in urlList:
        driver.get(url)

        getLargeListing(driver)
        sleep(0.5)
        sortFloat(driver)
        sleep(0.5)

        searchResults = driver.find_elements(By.CLASS_NAME,"market_listing_row")

        del searchResults[0]
        #removes the first part of listing that doesn't include any item just (it is a header)
        i = 1;

        for listing in searchResults:
            value = getFloat(driver, listing)
            price = getPrice(driver, listing)
            name = getName(driver, listing)
            if value < 0.3 and price < 0.24:
                print(i,":  ",name," float =",value," for",price,"E")
            else:
                print(i,":  ",name," float =",value," for",price,"E")
            i = i + 1; 

        print("______________________________________________________________")
        print("______________________________________________________________")

 


