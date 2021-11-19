from selenium import webdriver
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
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


s = Service(r"/home/mauricetjmurphy/Documents/Projects/211010_Twitter_Bot/env/bin/geckodriver.exe")
driver = webdriver.Firefox(service=s)
# os.environ['PATH'] += "env/bin/chromedriver.exe"
# ser = Service("/usr/local/bin/chromedriver.exe")
# op = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=ser, options=op)
# driver = webdriver.Firefox(executable_path=r"/home/mauricetjmurphy/Documents/Projects/211010_Twitter_Bot/env/bin/geckodriver.exe")

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")
# driver = webdriver.Chrome(service=ser,chrome_options=chrome_options)


driver.maximize_window()


user = os.environ.get("TWITTER_USERNAME")
password = os.environ.get("TWITTER_PASSWORD")
phone = os.environ.get("TWITTER_PHONE")


def login():
    driver.get("http://twitter.com/login")

    print( driver.title )
    time.sleep(5)
    inputElement1 = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")
    time.sleep(1)
    inputElement1.send_keys(user)
    time.sleep(1)
    button1 = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
    button1.click()

    try:
        time.sleep(1)
        inputElement2 = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")
        time.sleep(1)
        inputElement2.send_keys(phone)
        time.sleep(1)
        button2 = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
        button2.click()
        time.sleep(1)
    except:
        pass

    time.sleep(1)
    inputElement3 = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div/input")
    time.sleep(1)
    inputElement3.send_keys(password)
    time.sleep(1)
    button3 = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
    button3.click()
    time.sleep(5)

    
def stats():
    following = "0"
    followers = "0"
    
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



def followVisible():
    run = True
    while run:
        count = 0
        time.sleep(2)
        arr = getFollowButtons()
        
        if len(arr) < 4:
            print(f'There are only {len(arr)} on the page')
            print('Scrolling...')
            scrollPage()
        else:
            print(f'There are {len(arr)} left to follow on this page')
            for i,el in enumerate(arr):
                try:
                    el.click()
                    print(f'Click {i}')
                    count += 1
                    time.sleep(1)
                except ElementClickInterceptedException as e:
                    print(e)
                    print('Overload! Sleeping for 15 minutes...')
                    time.sleep(10)
                    driver.refresh()
                    time.sleep(3)
                    break
                except Exception as e:
                    print(e)
                    break
        print('Scrolling...')
        if len(arr) > 30:
            run = False
        elif len(arr) == 0:
            print('Scrolling...')
            scrollPage()
            time.sleep(2)
        else:
            run = True


def likeVisible():
    run = True
    while run:
        count = 0
        time.sleep(2)
        arr = getLikeButtons()
        print(arr)
        print(f'There are {len(arr)} left to Like on this page')
        for i,el in enumerate(arr):
            try:
                print(f'Click {i}')
                el.click()
                count += 1
                time.sleep(1)
            except ElementClickInterceptedException as e:
                print(e)
                print('Overload! Sleeping for 15 minutes...')
                time.sleep(5)
                driver.refresh()
                time.sleep(3)
                break
            except Exception as e:
                print(e)
                break
        if len(arr) > 30:
            run = False
        elif len(arr) == 0:
            print('Scrolling...')
            scrollPage()
            time.sleep(2)
        else:
            run = True
     
        

def scrollPage():
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)


def navToMainPage(search_term):
    driver.get("https://twitter.com/search?q=" + search_term + "&src=typed_query")
    time.sleep(5)

    cookiesCloseBtn = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/span/span')
    cookiesCloseBtn.click()
    time.sleep(2)


def navToFollowersPage(search_term):
    driver.get("https://twitter.com/search?q=" + search_term + "&src=typed_query")
    time.sleep(5)

    peopleLink = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div')
    peopleLink.click()
    time.sleep(3)

    pageLink = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[3]/div/div/div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span/span')
    pageLink.click()
    time.sleep(3)

    followersLink = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[5]/div[2]/a')
    followersLink.click()
    time.sleep(3)

    cookiesCloseBtn = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/span/span')
    cookiesCloseBtn.click()
    time.sleep(2)


def getFollowButtons():
    followButtons = driver.find_elements_by_xpath("//span[text()='Follow']")
    return followButtons


def getLikeButtons():
    likeButtons = driver.find_elements_by_xpath("//div[@data-testid = 'like']")
    return likeButtons

   



login()

try:
    WebDriverWait(driver, 10).until(EC.title_contains("Home"))
    print('Successful Login!')
finally:
    pass

# navToMainPage('rarible')
# for i in range(0, 8):
#     print(f'Starting session {i+1} of 8')
#     likeVisible()
#     scrollPage()
    

navToFollowersPage('SolanaBananas')
for i in range(0, 8):
    print(f'Starting session {i+1} of 8')
    followVisible()
    scrollPage()
    


driver.quit()

