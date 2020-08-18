import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from config import executable_path
# import pymongo
import copy
import time

def scrape ():

    executable_path1 = {'executable_path': executable_path}
    browser = Browser('chrome', **executable_path1, headless=False)

    # scrape 1
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(10)

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    # find the latest news title and paragraph text

    slide_soup = soup.find(class_='slide')
    title_news = slide_soup.find("div", class_='content_title').text
    print(title_news)

    paragraph = soup.find('div',class_="article_teaser_body").text
    print(paragraph)


# scrape 2
    executable_path1 = {'executable_path': executable_path}
    browser = Browser('chrome', **executable_path1, headless=False)
    
    url1='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)
    time.sleep(10)

    browser.find_by_css('button fancybox')

    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')
    pictures = soup1.find('footer')
    image_url = pictures.find('a', class_='button fancybox')
    image_url1 = image_url['data-fancybox-href']

        
    print(f"https://www.jpl.nasa.gov{image_url1}")
    featured_image_url = 'https://www.jpl.nasa.gov'+image_url1
    featured_image_url

    # scrape 3
    url2='https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)
    time.sleep(10)
    tweet_html = browser.html

    soup2 = BeautifulSoup(tweet_html, 'html.parser')

    print(soup2.prettify())

    weather = soup2.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text
    print(weather)

    # scrape 4
    url3 = 'https://space-facts.com/mars/'
    table = pd.read_html(url3)
    table

    df = table[0]
    df.columns = ['description','value']
    df

    html_data = df.to_html()
    html_data

    # scrape 5
    url4='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    time.sleep(10)

    soup4 = BeautifulSoup(browser.html, 'html.parser')
    print(soup4.prettify())

    
    description = soup4.find_all('div',class_="description")

    hemisphere_dic = {}
    hemisphere_image_urls = []

    for each in description:
        headline = each.h3

        title = headline.text
   
        img_urlz ='https://astropedia.astrogeology.usgs.gov/download'+each.a['href']+'.tif/full.jpg'
        img_urlx = img_urlz.replace('/search/map',"")
        print(img_urlx)

        print(title)
  

        hemisphere_dic['title'] = title
        hemisphere_dic['img_url'] = img_urlx

        hemisphere_image_urls.append(hemisphere_dic)


        hemisphere_dic = {}


    print(hemisphere_image_urls)

    # create dictionary to be pulled by app.py
    
    mars_dict = {
        'news_title': title_news,
        'news_p': paragraph,
        'featured_image_url': featured_image_url,
        'weather_data': weather,
        'facts_data': html_data,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    browser.quit()

    return mars_dict

