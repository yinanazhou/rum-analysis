from Scraper import Scraper

scraper = Scraper(url='https://rumratings.com/rum', sleep=10)
# next_url = scraper.scrape_first_page('./data/')

scraper.scrape_to_csv('https://rumratings.com/rum?page=354', './data/', pn=354)

