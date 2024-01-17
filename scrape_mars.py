from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape():

    manager = ChromeDriverManager().install()
    executable_path = {'executable_path': manager}
    browser = Browser('chrome', **executable_path, headless=False)

    mars = {}

    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    image_url = 'https://spaceimages-mars.com'
    browser.visit(image_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('img', class_ = 'headerimage fade-in')['src']
    featured_image_url = 'https://spaceimages-mars.com/' + image

    facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(facts_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    table = pd.read_html(facts_url)[0]
    table.set_index(0, inplace=True)
    table.index.name = 'Description'
    table.rename(columns={1:'Mars', 2:'Earth'}, inplace=True)
    table_html = table.to_html()

    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []
    images = soup.find_all('div', class_='item')
    for image in images:
        title = image.h3.text
        img_url = hem_url + image.img['src']

        hemisphere_image_dict = {
            'title': title,
            'img_url': img_url
        }
        
        hemisphere_image_urls.append(hemisphere_image_dict)
    
    mars['news_title'] = news_title
    mars['news_p'] = news_p
    mars['featured_image_url'] = featured_image_url
    mars['table'] = table_html
    mars['hemisphere_images'] = hemisphere_image_urls

    browser.quit()

    return mars