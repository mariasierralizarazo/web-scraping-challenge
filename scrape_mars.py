from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

def scrape():
    # Dictionary for returning
    information = dict()
    # Getting news title and text
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find('div',class_="list_text")
    title = article.a.text
    paragraph = soup.find('div',class_="article_teaser_body").text
    information = {'News title': title, 'News text': paragraph}
    browser.quit()
    # Getting feature image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    src = browser.find_by_tag('article')['style']
    src = src.replace('background-image: url("','')
    src = src.replace('");','')
    image_src = "https://www.jpl.nasa.gov" + src 
    information.update({"Image source":image_src})
    browser.quit()
    # Getting table 
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    mars_table = tables[0]
    mars_table = mars_table.rename(columns = {0:"Parameter",1:"Value"})
    html_mars_table = mars_table.to_html(index = False)
    information.update({"Table code": html_mars_table})
    # Getting hemispheres images
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_img = soup.find_all('div', class_='item')
    browser.quit()
    images_list = list()
    hemisphere = dict()
    for i in range(len(hemisphere_img)):
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)
        url = "https://astrogeology.usgs.gov" + (hemisphere_img[i].a["href"])
        browser.visit(url)
        image = browser.find_by_text('Sample')
        image = image['href']
        title = browser.find_by_tag('h2')
        title = title.text
        hemisphere = {'title': title, "img_url":image}
        images_list.append(hemisphere)
        browser.quit()
    information.update({"Images list":images_list})
    return(information)

print(scrape())
