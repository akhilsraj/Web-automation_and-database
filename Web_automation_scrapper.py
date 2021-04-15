from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import time
from bs4 import BeautifulSoup
import requests
import pymongo
result = []
PATH = "C:\Program Files (x86)\chromedriver"
class Linkedin:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.bot=webdriver.Chrome(PATH)
    def login(self):
        bot=self.bot
        bot.get("https://www.linkedin.com/uas/login")
        time.sleep(2)
        email=bot.find_element_by_id("username")
        email.send_keys(self.username)
        password=bot.find_element_by_id("password")
        password.send_keys(self.password)
        time.sleep(2)
        password.send_keys(Keys.RETURN)
        time.sleep(2)
    def search(self,input_name):
        bot = self.bot
        self.input_name = input_name.split()
        x = ""
        num_20s = len(self.input_name)
        if(num_20s == 1):
            x = self.input_name[0] + '%20'
        else:
            for i in range(num_20s):
                if(i == (num_20s) - 1):
                    x = x + self.input_name[i]
                else:
                    x = x + self.input_name[i] + '%20'
        bot.get('https://www.linkedin.com/search/results/people/?keywords={name}&origin=GLOBAL_SEARCH_HEADER'.format(name = x))
       
        time.sleep(5) 
        for name in bot.find_elements_by_xpath('//*[@id="main"]/div/div/div[2]/ul/li[1]/div/div/div[2]/div[1]/div/div[1]/span/div/span[1]/span/a'):
            name.click()
            time.sleep(1)
        time.sleep(7)
    def scroll(self):
        bot = self.bot
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = bot.execute_script("return document.body.scrollHeight")

        while True:
            bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = bot.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
                
    def scrape(self):
        bot = self.bot
        extracted_data = []
        src = bot.page_source
        soup = BeautifulSoup(src, 'lxml')
        text = soup.find('div',{'class':'flex-1 mr5 pv-top-card__list-container'})
        name_of_search = text.find_all('ul')
        for string in name_of_search:
            extracted_data.append(string.find('li').get_text().strip())
        time.sleep(3)
        extracted_data.append(text.find('h2').get_text().strip())
        text = soup.find('section',{'id':'experience-section'})
        ui_tags = text.find('ul')
        li_tags = ui_tags.find('div')
        a_tags = li_tags.find('a')
        extracted_data.append(a_tags.find('h3').get_text().strip())
        for i in a_tags.find_all('p'):
            extracted_data.append(i.get_text().strip())
        extracted_data.append(a_tags.find_all('h4')[0].find_all('span')[1].get_text().strip())
        return(extracted_data)
        
        
x = input().split(',')
load=Linkedin("akhils.ec18@bmsce.ac.in","Mousse Cake1")
load.login()
for i in x:
    mongo_uri = "mongodb://localhost:27017/"  
    client = pymongo.MongoClient(mongo_uri)
    mydb = client['linkedin_profiles']
    information = mydb.linkedininformation
    load.search(i)
    load.scroll()
    result = load.scrape()
    dicts = [{
        'Name' : result[0],
        'Place' : result[1],
        'Current Job' : result[2],
        'Expierience' : result[-1],
        }]
    information.insert_many(dicts)
    print(dicts)

    
    
