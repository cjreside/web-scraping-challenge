# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"/usr/local/bin/chromedriver": "chromedriver.exe"}
    return Browser("chrome", executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars News URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image to be scraped
    main_url = "https://www.jpl.nasa.gov"
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(featured_image_url)
    html_image = browser.html
    soup = BeautifulSoup(html_image, "html.parser")
    # Retrieve featured image link
    image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    image_url = main_url + image_url

    # Mars facts to be scraped, converted into html table
    url="https://space-facts.com/mars/)"
    mars_table=pd.read_html(url)
    ctable=mars_table[0]
    final_table=ctable.rename(columns={0:'Description',1: "value"})
    html = final_table.to_html()
    
    # Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    # Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')
    hemisphere_image_urls = []
    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)        
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url        
        hemisphere_image_urls.append(image_dict)


    # Mars Dic
    mars_dict = {
            "news_title": news_title,
            "news_p": news_paragraph,
            "featured_image_url": featured_image_url,
            "fact_table": str(html),
            "hemisphere_images": hemisphere_image_urls
        }

    return mars_dict

if __name__ == "__main__":
   print(scrape())
