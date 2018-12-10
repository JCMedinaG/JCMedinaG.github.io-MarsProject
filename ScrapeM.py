#import dependencies
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
######################## NASA Mars News ######################## 
    browser = init_browser()


    # Visit the site
    url_marsnews = 'https://mars.nasa.gov/news/'
    browser.visit(url_marsnews)
    time.sleep(2)

    # scrape the page
    html_content = browser.html

    # parse the html and store the results in a beautifulsoup object
    soup = BeautifulSoup(html_content,'lxml')

    # retrieve the latest article
    news_articles = soup.find_all('li',class_='slide')
    first_article = news_articles[0]

    # get the date for the latest news article
    news_date = first_article.find('div',class_='list_date')
    news_date = news_date.get_text()

    # get the title text for the latest news article 
    news_title = first_article.find('div',class_='content_title')
    news_title = news_title.get_text()
    news_title = news_title.strip()

    # get the paragraph text for the latest news article 
    news_para = first_article.find('div',class_='article_teaser_body')
    news_para = news_para.get_text()
    news_para = news_para.strip()

    # marsNews dictionary
    marsNews = {'marsNewsDatepublished':news_date,
                'marsNewsTitle':news_title,
                'marsNewsContents':news_para}

######################## JPL Mars Space Images - Featured Image ######################## 

    # Visit the NASA Jet Propultion Laboratory site
    # Jet Propultion Laboratory

    
    url_jplMars = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jplMars)
    time.sleep(2)

    # navigate to the full image using splinter
    image = browser.find_by_id('full_image')
    image.click()
    time.sleep(2)

    # parse the html and store the results in a beautifulsoup object
    html = browser.html
    soup = BeautifulSoup(html,'lxml')

    # get the image url for the featured images
    #fancybox-lock > div > div.fancybox-inner.fancybox-skin.fancybox-dark-skin.fancybox-dark-skin-open > img
    featured_image_url = soup.find('div',class_='fancybox-inner')
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url.find('img',class_='fancybox-image')['src']


######################## Mars Weather Tweet######################## 

    # Visit the Mars Weather twitter account

    url_tweetMars = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_tweetMars)
    time.sleep(2)

    # parse the html and store the results in a beautifulsoup object
    html = browser.html
    soup = BeautifulSoup(html,'lxml')

    # get the first tweet from the tweet feeds
    #timeline > div > div.stream
    tweets = soup.find('div',class_='stream').find_all('li',class_='js-stream-item')
    first_tweet = tweets[0]
    first_tweet_text = first_tweet.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    first_tweet_text = first_tweet_text.get_text()

######################## Mars Facts######################## 

    # Visit the Mars Weather twitter account
    url_marsFacts = 'https://space-facts.com/mars/'

    # pandas.read_html to parse the table data
    df = pd.read_html(url_marsFacts)[0]
    df.columns = ['Description','Value']

    # pandas.to_html to convert the pandas dataframe to HTML
    html_table = df.to_html(header=True,index=False)
 
######################## Mars hemisphere ######################## 

    # Visit the USGS Astrogeology site
    url_usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # empty list to store the results
    hemisphere_image_urls =[]

    # loop through each link(Hemispere)
    for x in list(range(4)):
        browser.visit(url_usgs)
        time.sleep(2)
        links = browser.find_by_css('div.item > div.description > a')
        links[x].click()
        time.sleep(2)
        html = browser.html
        soup = BeautifulSoup(html,'lxml')
        #splashy > div.wrapper > div.container > div.content > section > h2.title
        title = soup.find('h2',class_='title').get_text()
        #wide-image > img
        img_url = soup.find(id="wide-image").find('img',class_='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov' + img_url
        hemisphere_image_urls.append({'title':title,'img_url':img_url})

######################## dictionary containing all of the scraped data ######################## 

    scrappedDict = {'marsNews': marsNews,
            'jplImage': featured_image_url,
            'marsWeatherTweet':first_tweet_text,
            'marsFactsTable':html_table,
            'marsHemispheres':hemisphere_image_urls}

    return scrappedDict


if __name__ == "__main__":
    scrape()