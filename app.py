from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path=r'env/bin/geckodriver.exe')

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        # Pause app for 3 seconds to wait for page load
        time.sleep(3)
        sign_in = bot.find_elements_by_xpath("/html/body/div/div/div/div/main/div/div/div[1]/div[1]/div/div[3]/div[4]/span/span")
        sign_in[0].click()
        


    def like_tweet(self, hashtag):
        # Search for a URL
        bot = self.bot
        bot.get('https://twitter.com/search?q='+hashtag+'&src=typed_query')
        for i in range(1, 10):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight')
            time.sleep(3)
            tweets = bot.find_elements_by_xpath("//article[@id='data-testid']")
            print



test = TwitterBot('mauricetjmurphy@gmail.com', os.environ.get("TWITTER_PASSWORD"))
test.login()