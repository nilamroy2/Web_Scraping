#import dependencies
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


#creating the dictionary which will store data in Mongo
mars_dict = {}

#NASA Mars News
def scrape_mars_news():
    try:

        browser = init_browser()
        news_url = 'https://mars.nasa.gov/news/'
        browser.visit(news_url)

        #time.sleep(1)
# HTML Object
        html = browser.html

# Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
# Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text
#put it in a Dictionary
        mars_dict['news_title'] = news_title
        mars_dict['news_paragraph'] = news_p
 # Return results
        return mars_dict
# Close the browser after scraping
    finally:

        browser.quit()
#Images
def scrape_mars_image():
     try:
         browser = init_browser()

#visit through splinter
         image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
         browser.visit(image_url)
# Go to 'FULL IMAGE', then to 'more info'
         #browser.click_link_by_partial_text('FULL IMAGE')
         #browser.click_link_by_partial_text('more info')

         #time.sleep(1)
# HTML Object
         html = browser.html

# Parse HTML with Beautiful Soup
         soup = BeautifulSoup(html, 'html.parser')
         image = soup.find("img", class_="thumb")["src"]
         featured_image_url = "https://www.jpl.nasa.gov" + image
       
#retriving background images from thumb class
         #featured_img_url = soup.find('figure', class_='lede').a['href']
         #featured_img_full_url = f'https://www.jpl.nasa.gov{featured_img_url}'
         #return featured_img_full_url
         mars_dict['featured_image_url'] = featured_image_url
# Return results
         return mars_dict
# Close the browser after scraping
     finally:
        browser.quit()

#Mars Weather
def scrap_mars_weather():

     try:
# Initialize browser 
        browser = init_browser()
# Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        #time.sleep(1)
# HTML Object 
        html_weather = browser.html

# Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

# Find all elements that contain tweets
        latest_tweet = soup.find('p', class_='TweetTextSize').text
       
# Dictionary entry from WEATHER TWEET
        mars_dict['weather_tweet'] = latest_tweet
# Return results        
        return mars_dict
     finally:
# Close the browser after scraping
         browser.quit()
#Mars Property
def scrape_mars_fact():
    # Visit Mars facts url 
    facts_url = 'https://space-facts.com/mars/' 
     # Use Panda to `read_html` to parse the url  
    mars_facts = pd.read_html(facts_url)
    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[1]
    #assigning the column value
    mars_df.columns=['Property','value']
    #setting the index to the property column
    mars_df.set_index('Property',inplace=True)
    #save the html value inside data
    data = mars_df.to_html()
    #put the value inside the dictonary
    mars_dict['mars_facts']=data
    return mars_dict

 
#Mars Hemisphere
def scrape_mars_hemisphere():
     try:
#initialize browser
         browser = init_browser()
#visit hemisphere module through splinter
         hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
         browser.visit(hemispheres_url)
# HTML Object
         html_hemispheres = browser.html

# Parse HTML with Beautiful Soup
         soup = BeautifulSoup(html_hemispheres, 'html.parser')

#retrive the information under item class
         items = soup.find_all('div', class_='item')

# Create empty list for hemisphere 
         hemisphere_image_urls = []
# Store the main_ul 
         hemispheres_main_url = 'https://astrogeology.usgs.gov'

# Loop through the items previously stored
         for i in items: 
    # Store title
             title = i.find('h3').text
    
    # Store link that leads to full image website
             part_img_url = i.find('a', class_='itemLink product-item')['href']
    
    #navigate the page which contains the full image website 
             browser.visit(hemispheres_main_url + part_img_url)
    
    # HTML Object of individual hemisphere information website 
             part_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
             soup = BeautifulSoup(part_img_html,'html.parser')
    
    # Retrieve full image source 
             img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a list of dictionaries 
             hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

# Display hemisphere_image_urls
         mars_dict['hemisphere_image_urls']=hemisphere_image_urls
         return mars_dict
     finally:
# Close the browser after scraping
         browser.quit()