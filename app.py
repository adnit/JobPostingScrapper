import requests
import pymysql
import time
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# database connection
connection = pymysql.connect(host="localhost",user="root",passwd="",database="jobsdb")
cursor = connection.cursor();


def loadPage():
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  # download chromedriver based on the version of chrome u have https://chromedriver.chromium.org/downloads
  driver = webdriver.Chrome('./chromedriver',options=chrome_options)
  driver.get('https://ofertapune.net/')
  # button = driver.find_element_by_class_name("load_more_jobs") // clicks the load more jobs button
  # button.click()
  # time.sleep(3)
  # button.click()
  # time.sleep(3)
  # button.click()
  html = driver.page_source
  scrapeListings(html)

# inserts scrapped data to database
def insertdb(logo, titulli, lokacioni, deadline, company, description, link):
  connection = pymysql.connect(host="localhost",user="root",passwd="",database="jobsdb")
  cursor = connection.cursor();

  mysql_insert = """
  INSERT INTO Jobs (LOGO, TITULLI, LOKACIONI, DEADLINE, COMPANY, DESCRIPTION, OGLINK)
  VALUES (%s, %s, %s, %s, %s, %s, %s)
  """
  record = (logo, titulli, lokacioni, deadline, company, description, link)
  cursor.execute(mysql_insert, record)
  connection.commit()
  print('Entry: ' + titulli + ' inserted successfully')

def closeConnection():
  connection.close()

# creates table
Jobs = """
CREATE TABLE IF NOT EXISTS Jobs(
ID INT(20) PRIMARY KEY AUTO_INCREMENT,
LOGO VARCHAR(200) NOT NULL,
TITULLI VARCHAR(100) NOT NULL,
LOKACIONI VARCHAR(40) NOT NULL,
DEADLINE VARCHAR(20) NOT NULL,
COMPANY VARCHAR(60) NOT NULL,
DESCRIPTION TEXT NOT NULL,
OGLINK  VARCHAR(200) NOT NULL)
"""

Droptable = """DROP TABLE Jobs"""
# excutes database 'queries'
cursor.execute(Droptable)
cursor.execute(Jobs)

def scrapeListings(source):
  soup = BeautifulSoup(source, 'lxml')
  jobResults = soup.find_all('a', {'class': 'job_listing-clickbox'})
  for job in jobResults:
    getJobInfo(job.get('href'))
  closeConnection()

def getJobInfo(listing):
  logo = ''
  titulli = ''
  lokacioni = ''
  deadline = ''
  company = ''
  desc = ''
  href = listing
  result = requests.get(listing)
  if '200' in str(result):
    source = result.content
    soup = BeautifulSoup(source, 'lxml')
    logo = soup.find('img', {'class':'company_logo'}).get('src').strip()
    titulli = soup.find('h1', {'class':'page-title'}).string.strip()
    lokacioni = soup.find('a', {'class':'google_map_link'}).string.strip()
    deadline = soup.find('li', {'class':'application-deadline'}).text.strip('Skadon: ')
    company = soup.find('li', {'class':'job-company'}).text.strip()
    desc = soup.find('div', {'class': 'job_listing-description job-overview col-md-10 col-sm-12'}).get_text().strip()
  insertdb(logo,titulli[0:100], lokacioni, deadline, company, desc, href)

loadPage()