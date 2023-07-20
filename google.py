import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import selenium.common
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

ua = UserAgent().random
options = Options()
options.add_argument(f"user-agent={ua}")
service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(options = options, service= service)
def request():
    driver.get(url='https://docs.google.com/forms/d/e/1FAIpQLSdhd0J0Od4Rw-V32wUIMrq6h7WRlo9lvQH_AoQk9JJZMVXJ3g/viewform?usp=sf_link')
    time.sleep(3)
    if driver.title == "SF renting research":
        print("got it")
        return True
    else:
        time.sleep(5)
        driver.quit()
        request()
request()
number=0
def give_response():
    global number
    elements = driver.find_elements(by='css selector', value='input.whsOnd')
    list = ['abey', 'asmare', 'bukayaw']
    i=0
    for element in elements:
        element.send_keys(list[i])
        element.submit()
        i+=1
        if elements.index(element) == 2:
            element.send_keys(Keys.TAB, Keys.ENTER)
    number+=1
    print(number)
    if number <3:
        time.sleep(3)
        driver.find_element(by='css selector', value='.idZHHb div a').click()
        give_response()

give_response()
time.sleep(3)
# time.sleep(5)
# driver.find_element(by='css selector', value='#ResponsesView .cd29Sd').click()

time.sleep(300)
