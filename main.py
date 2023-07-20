from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from fake_useragent import UserAgent
import random


GOOGLE_DOCS = 'https://docs.google.com/forms/d/e/1FAIpQLSfFFAoS8xVKqq_xo_EtMI797ZcAlnFFtDgfRHd4WBFrNQoygg/viewform'
URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A38.34835138843188%2C%22east%22%3A-120.9776405234375%2C%22south%22%3A37.19775491358151%2C%22west%22%3A-123.8890174765625%7D%2C%22mapZoom%22%3A8%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22baths%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

ua = UserAgent().random
options = Options()
options.add_argument(f"user-agent={ua}")
service = Service(executable_path="C:\Development\chromedriver.exe")
driver = webdriver.Chrome(options=options, service= service)
driver.set_window_size(1920, 1050)
sleep(1)
driver.get(URL)
sleep(10)

#try to get the first element but if it did not found get the second element and be ready to interact with it
try:
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(by="xpath", value='/html/body/div[1]/div[5]/div/div/div[1]/div[1]/ul'))
except exceptions.NoSuchElementException:
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(by="xpath", value='/html/body/div[1]/div[5]/div/div/div[1]/div[1]/ul/li[2]/article/div/div[2]/div[2]/a'))

#perform lazy loading with random time delay
def perform_lazy_loading():
    sleep(5)
    for i in range(13):
        driver.find_element(by='xpath', value='/html/body/div[1]/div[5]/div/div/div[1]/div[1]/ul/li[1]/article/div/div[2]/div[2]/a').send_keys(Keys.PAGE_DOWN)
        sleep(random.randint(1,2))

#get the source file with beautiful soup
perform_lazy_loading()
soup = BeautifulSoup(driver.page_source,'html.parser')



#Get all the links of the homes
def get_home_links()->list:
    links = []
    for link in soup.find_all(name="a", class_ = "property-card-link", attrs={"data-test":'property-card-link'}):
        link = link['href']
        if "https://www.zillow.com" not in link:
            new_val = f"https://www.zillow.com{link}"
        else:
            new_val = link
        if new_val not in links:
            links.append(new_val)
    return links


#get the prices of the items
def get_home_prices()->list:
    prices = []
    for p in soup.findAll(name='span', attrs={"data-test": "property-card-price"}):
        p = p.getText()
        if "/" in p:
            new_val = p.split('/')
        else:
            new_val = p.split('+ ')
        prices.append(new_val[0])
    return prices

#get all the address of the items
def get_home_address()->list:
    home_adress = []
    for home in soup.findAll(name='address', attrs= {"data-test": "property-card-addr"}):
        home =  home.getText()
        home_adress.append(home)
    return home_adress


sleep(3)
#created 1 dictionary that has the address, price and link lists
home = {
    "address": get_home_address(),
    "price": get_home_prices(),
    "link": get_home_links()
}
#after getting the datas go to the google docs url and fill it using selenium
def request():
    driver.get(url='https://docs.google.com/forms/d/e/1FAIpQLSdhd0J0Od4Rw-V32wUIMrq6h7WRlo9lvQH_AoQk9JJZMVXJ3g/viewform?usp=sf_link')
    sleep(3)
    if driver.title == "SF renting research":
        print("got it")
        return True
    else:
        sleep(5)
        driver.quit()
        request()
request()

def give_response():
    for i in range(0, len(home['address'])):
            input_fields = driver.find_elements(by='css selector', value='input.whsOnd')
            input_fields[0].send_keys(home['address'][i])
            input_fields[0].submit()

            input_fields[1].send_keys(home['price'][i])
            input_fields[1].submit()

            input_fields[2].send_keys(home['link'][i])
            input_fields[2].submit()
            input_fields[2].send_keys(Keys.TAB, Keys.ENTER)
            sleep(3)
            driver.find_element(by='css selector', value='.idZHHb div a').click()
            sleep(3)
            print(i)

give_response()

driver.quit()
# /html/body/div/div[3]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input
# /html/body/div/div[3]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input
# /html/body/div/div[3]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input
# .c2gzef a
