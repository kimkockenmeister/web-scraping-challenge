from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd 

def init_browser():
# @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path={'executable_path':''}
    path= r'/Users/kimkockenmeister/Downloads/chromedriver-3'
    return Browser("chrome", executable_path=path, headless = True)

def scrape():
    browser = init_browser()
   
    # Visit url
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Store data in a dictionary
    mars_dict = {}
    
    #web scrape news
    article = soup.find("div", class_='list_text')
    news_title = article.find("div",class_="content_title").text
    news_paragraph = article.find("div", class_="article_teaser_body").text
    
    mars_dict['news_title'] = news_title
    mars_dict['news_paragraph'] = news_paragraph 
    
    #web scrape image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    
    time.sleep(2)
    
    html = browser.html
    soup = bs(html, "html.parser")
    featured_image=soup.find_all('article',class_="carousel_item")[0]['style']
    featured_image=featured_image.strip("background-image: url('")
    featured_image=featured_image.strip("');")
    featured_image=featured_image.strip("')")
    base_url="https://www.jpl.nasa.gov"
    featured_image_url=base_url+featured_image
    mars_dict["featured_image"] = featured_image_url
    
   
    #web scrape facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    time.sleep(1)
    #Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(facts_url)

    facts_df = tables[0]
    facts_df.columns = [" ", "Mars"]

    mars_facts=facts_df.to_html(index=False)
    mars_dict["mars_facts"] = mars_facts

    
    #web scrape hemisphere
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    mars_dict["hemisphere_img_url"] = mars_hemisphere

    print(mars_dict)
    return mars_dict  

    if __name__ == "__main__":
        print(scrape())
