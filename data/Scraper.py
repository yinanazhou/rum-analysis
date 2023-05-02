from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.request import Request, urlopen
import os


class Scraper:
    def __init__(self, url, sleep=10):
        self.url = url
        self.sleep = sleep
        self.base_url = self.url.rsplit('/', 1)[0]

    def scrape_first_page(self, folder, pn=1):
        if not os.path.exists(folder):
            os.makedirs(folder)

        to_save = pd.DataFrame()
        req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')
        next_url = self.base_url + soup.find('a', rel='next').get('href')

        to_save = to_save.append(self.get_page_content(soup))
        to_save.to_csv(folder + 'page_' + str(pn).zfill(3) + '.csv', index=False)
        return next_url

    def scrape_to_csv(self, next_url, folder, pn=2):
        if not os.path.exists(folder):
            os.makedirs(folder)

        while next_url:
            to_save = pd.DataFrame()
            print('Page: ', pn)
            req = Request(next_url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'html.parser')
            if soup.find('a', rel='next'):
                next_url = self.base_url + soup.find('a', rel='next').get('href')
            else:
                next_url = None

            to_save = to_save.append(self.get_page_content(soup))
            to_save.to_csv(folder+'page_'+str(pn).zfill(3)+'.csv', index=False)
            pn += 1

        print('Done!')

    def get_page_content(self, soup):
        page_content = pd.DataFrame()
        rums = soup.find_all('a', class_="thumbnail")

        for rum in rums:
            rum_info = {}
            rum_url = self.base_url + rum.get('href')
            rum_info["URL"] = rum_url
            print(rum_url)
            rum_req = Request(rum_url, headers={'User-Agent': 'Mozilla/5.0'})
            rum_page = urlopen(rum_req).read()
            rum_soup = BeautifulSoup(rum_page, 'html.parser')

            # brand details
            section = rum_soup.find('div', class_="grid-sidebar")
            details = section.find_all('span', class_='w-3/5')
            detail_name = section.find_all('span', class_='w-2/5')
            for i, detail in enumerate(details):
                rum_info[detail_name[i].text] = detail.text

            # location
            section = rum_soup.find('p', class_="info")
            location = section.find('a', class_='hero-edit-link')
            if 'location' in location.get('href'):
                rum_info['Location'] = location.text

            # rating
            section = rum_soup.find('div', class_='u-margin-none dark:text-neutral-300')
            if section:
                rum_info['Score'] = section.find('big').text
                rum_info['nRatings'] = section.find('span', style='white-space: nowrap').text.split(' ratings')[0]

            # price
            section = rum_soup.find('div', class_='mobilebottlehead my-2').find('a', class_='c-button')
            if section:
                rum_info['Price'] = section.text.split('$')[-1]

            page_content = page_content.append(pd.DataFrame(rum_info, index=[0]))

            time.sleep(self.sleep)
        return page_content









