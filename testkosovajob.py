import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 

def loadPage():
  chrome_options = Options()
  #chrome_options.add_argument("--disable-extensions")
  #chrome_options.add_argument("--disable-gpu")
  #chrome_options.add_argument("--no-sandbox") # linux only
  chrome_options.add_argument("--headless")
  # chrome_options.headless = True # also works
  driver = webdriver.Chrome('./chromedriver',options=chrome_options)
  #driver = webdriver.Chrome(executable_path='./chromedriver')
  driver.get('https://kosovajob.com/')
  # button = driver.find_element_by_class_name("load_more_jobs")
  # button.click()
  # time.sleep(3)
  # button.click()
  # time.sleep(3)
  # button.click()
  html = driver.page_source
  scrapeListings(html)

def scrapeListings():
  source = requests.get('https://kosovajob.com/').content
  soup = BeautifulSoup(source, 'lxml')
  jobResults = soup.find_all('div', {'class': 'lists'})
  for jobDiv
  jobs = jobResults.find('a')
  for job in jobs:
    print(job.get('href'))
scrapeListings()
