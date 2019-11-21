import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser



def scrape():
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser = Browser('chrome', headless=True)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.quit()
    head = soup.find_all("div", class_="content_title")[0].text
    body = soup.find_all("div", class_="article_teaser_body")[0].text
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser = Browser('chrome', headless=True)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.quit()
    featured_image_url = 'https://www.jpl.nasa.gov' + soup.find_all("a", class_= 'fancybox')[1]["data-fancybox-href"]
    url = 'https://twitter.com/marswxreport?lang=en'
    browser = Browser('chrome', headless=True)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.quit()
    weather = soup.find("p", class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)
    table_df = table[0]
    table_df.columns = ['Variables', 'Values'] 
    table_df.set_index('Variables', inplace = True)
    table_html = table_df.to_html()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser = Browser('chrome', headless=True)
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.quit()
    links = []
    a = soup.find_all("a", class_='itemLink product-item')
    for x in range(len(a)):
        link = 'https://astrogeology.usgs.gov' +a[x]['href']
        if link not in links:
            links.append(link)
    hemi_image_url = []
    for x in range(len(links)):
        browser = Browser('chrome', headless=True)  
        browser.visit(links[x])
        html = browser.html
        soup = bs(html, 'html.parser')  
        browser.quit()
        url = 'https://astrogeology.usgs.gov' + soup.find('img', class_="wide-image")["src"]
        title = soup.find('h2', class_= 'title').text
        dic = {'title':title, 'img_url': url}
        hemi_image_url.append(dic)
    data = {
        'head':head,
        'body':body,
        'image':featured_image_url,
        'weather':weather,
        'table':table_html,
        'hems':hemi_image_url
    }
    return data