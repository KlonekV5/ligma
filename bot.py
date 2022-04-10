import os

try:
    import selenium
    import pyderman
except ImportError:
    print('Requirements not installed')
    os.system('pip install selenium')
    os.system('pip install pyderman')

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import json


login = 'ur login here'
passwd = 'ur passwd here'
times = int(input('how many lessons do u want to do?'))

driver_path = pyderman.install(browser=pyderman.chrome)
driver = webdriver.Chrome(executable_path=driver_path)

def logon():
    driver.get('https://lingos.pl/home/login')
    log_fld  = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/form/div[1]/input')
    psw_fld  = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/form/div[2]/input')
    sub_btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/button')

    # user login in browser
    log_fld.send_keys(login)
    psw_fld.send_keys(passwd)
    sub_btn.click()
    time.sleep(3)


def lesson():
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/a').click()
    while driver.current_url != 'https://lingos.pl/students/start/finished':

        # do study
        if driver.current_url.startswith('https://lingos.pl/students/learning'):

            # adds new word
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div[2]/h4')
                ang = driver.find_element_by_xpath('/html/body/div[2]/div[2]/h3[1]').text
                pl = driver.find_element_by_xpath('/html/body/div[2]/div[2]/h3[2]').text
                data[pl] = ang
                driver.find_element_by_xpath('//*[@id="checkWordForm"]/form/button').click()

            # can't add new word
            except NoSuchElementException:
                pl = driver.find_element_by_xpath('/html/body/div[2]/div[2]/h3').text
                
                # it knows that word so it types it in
                if pl in data:
                    ans_fld = driver.find_element_by_xpath('//*[@id="answer"]')
                    ans_fld.send_keys(data[pl])
                    driver.find_element_by_xpath('//*[@id="nextBtn"]').click()

                # don't know that word so it adds it to dictionary
                else:
                    driver.find_element_by_xpath('//*[@id="nextBtn"]').click()
                    ang = driver.find_element_by_xpath('/html/body/div[2]/div[2]/h5[4]/span/strong').text
                    data[pl] = ang

        # it answered correctly so clicks 'next'
        elif driver.current_url == 'https://lingos.pl/students/checkAnswer/0,0':
            driver.find_element_by_xpath('//*[@id="next"]').click()
    time.sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)


def export(dic):
    export_file = open('data.json', 'w')
    json.dump(dic, export_file, indent=4)
    export_file.close()


def load():
    # checks if data.json file exists
    # if yes imports it as data / if no creates data dict
    if os.path.exists('data.json'):
        json_file = open('data.json', 'r')
        data = json.load(json_file)
        json_file.close()
    else:
        data = {}
    return data

data = load()
logon()
for _ in range(times):
    lesson()
export(data)
