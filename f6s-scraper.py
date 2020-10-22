import glob
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# VARIABLES
SCROLL_TIME = 1
urls = ['https://www.f6s.com/programs?keywords[]=cleantech&sort=open', 'https://www.f6s.com/programs?skills[]=769&sort=open', 'https://www.f6s.com/programs?keywords[]=waste&sort=open', 'https://www.f6s.com/programs?keywords[]=climate&sort=open', 'https://www.f6s.com/programs?keywords[]=water&sort=open',  'https://www.f6s.com/programs?keywords[]=environmental&sort=open', 'https://www.f6s.com/programs?skills[]=150529&sort=popular&sort_dir=desc']
driver = webdriver.Chrome('/usr/bin/chromedriver')

# SCRAPER
data = {}
company_name = []
name_set = set()
logo = []
location = []
link = []
twitter = []
sector = []
for url in urls:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    element = driver.find_element_by_tag_name('html')
    while not soup.find('div', class_='bordered-list-item result-item list-separator'):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_TIME)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

    cnt = int(soup.find(id='csProgramResultsCount').get_text().split()[0])
    companies = soup.find_all('div', class_='bordered-list-item result-item')
    for i in range(0, cnt):
        company = companies[i].find('div', class_='title').a
        if(company.get_text() in name_set):
            continue
        name_set.add(company.get_text())
        company_name.append(company.get_text())
        logo.append(companies[i].find('div', class_='organization-picture').a.img['src'])
        location.append(' '.join([str(x) for x in companies[i].find('div', class_='subtitle').span.get_text().split()]))
        sector.append(companies[i].find('div', class_='details').span.get_text()[18:])

        driver.find_element_by_tag_name('html').send_keys(Keys.CONTROL+"t")
        driver.get(company['href'])
        
        detailed_page = BeautifulSoup(driver.page_source, 'html.parser')
        site = detailed_page.find('a', class_='link-icon link-website fa-link')
        twt = detailed_page.find('a', class_='link-icon link-twitter fa-twitter-square')
        if site:
            link.append(site['href'])
        else:
            link.append(None)
        if twt:
            twitter.append(twt['href'])
        else:
            twitter.append(None)

        driver.find_element_by_tag_name('html').send_keys(Keys.CONTROL+"w")
        
# print(len(company_name))
# print(len(logo))
# print(len(location))
# print(len(sector))
# print(len(link))
# print(len(twitter))

data['company_name'] = company_name
data['logo'] = logo
data['location'] = location
data['sector'] = sector
data['link'] = link
data['twitter'] = twitter

df = pd.DataFrame.from_dict(data)
csv = df.to_csv('companies.csv', index=True)
