from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
import re
from os.path import expanduser
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


driver = webdriver.Firefox(executable_path=r'env/bin/geckodriver.exe')


user = os.environ.get("TWITTER_USERNAME")
password = os.environ.get("TWITTER_PASSWORD")


def login():
    driver.get("http://twitter.com/login")

    print( driver.title )
    time.sleep(5)
    inputElement1 = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")
    time.sleep(2)
    inputElement1.send_keys(user)
    time.sleep(2)
    button1 = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
    button1.click()
    time.sleep(2)
    inputElement2 = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/label/div/div[2]/div/input")
    time.sleep(2)
    inputElement2.send_keys(password)
    time.sleep(2)
    button2 = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
    button2.click()
    time.sleep(5)

    try:
        WebDriverWait(driver, 10).until(EC.title_contains("Home"))
        print( driver.title )
    finally:
        pass

def stats(screen_name):
    following = "0"
    followers = "0"
    driver.get(f"https://twitter.com/{screen_name}")
    time.sleep(5)
    data1 = driver.find_element_by_xpath("/html/body/div")
    m1 = re.search(data1.text, "\n(\d+) Following\n(\d)+Followers\n")
    if m1:
        following = m1.group(1)
        followers = m1.group(2)
    print("Following: " + following)
    print("Followers: " + followers)


def search(search_term):
    links = []

    driver.get("https://twitter.com/search?q=" + search_term + "&src=typed_query")
    time.sleep(5)

    users_who_posted = []
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[1]/a/div/div[2]/div/span").text)
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[2]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[1]/a/div/div[2]/div/span").text)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[7]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[1]/a/div/div[2]/div/span").text)
    for i in range(3,20):
        try:
            users_who_posted.append( driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[" + str(i) + "]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[1]/a/div/div[2]/div/span").text)
        except: 
            pass

    print(users_who_posted)


def followUsers(search_term):
    driver.get("https://twitter.com/search?q=" + search_term + "&src=typed_query")
    time.sleep(5)

    pageLink = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[3]/div/div/div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span/span')
    pageLink.click()
    time.sleep(3)

    followersLink = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[2]/a')
    followersLink.click()
    time.sleep(3)

    followersContainer = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section")
    followButtons = driver.find_elements_by_xpath("//*[contains(text(), 'Follow')]")

    for el in followButtons:
        el.click()
    
    print(followButtons)
    
    # buttonContainers = followersContainer.find_element_by_tag_name('span')
    # for el in buttonContainers:
    #     button = el.find


login()
followUsers('rarible')



time.sleep(1000)
driver.quit()

