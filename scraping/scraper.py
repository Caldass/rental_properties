import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

#beautiful soup and selenium objects

driver = webdriver.Chrome(executable_path='C:/Program Files/selenium/chromedriver.exe')

url = 'https://www.vivareal.com.br/aluguel/pernambuco/recife/apartamento_residencial/'

driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")

           
#Code to insert into df the scraping information as dicts
#Code found on https://stackoverflow.com/questions/41825868/update-python-dictionary-add-another-value-to-existing-key/41826126#41826126
def set_key(dictionary, key, value):
     if key not in dictionary:
         dictionary[key] = value
     elif type(dictionary[key]) == list:
         dictionary[key].append(value)
     else:
         dictionary[key] = [dictionary[key], value]


#dataframe with scraped data
df = {}


#follow the pages scraped
page = 0

#number of posts scraped
post_num = 0

#scrape while posts scraped < total posts possible
while post_num < int(soup.find('strong', attrs = {"class" : "results-summary__count js-total-records"}).text.replace('.','').strip()):
    
    #updates url after clicking page    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")

    #storing all properties in a list
    page_posts = [i for i in soup.find('div', attrs = {"class" : "results-list js-results-list"}).find_all('div', attrs = {"data-type" : 'property'})]
    
    #getting variables for each post
    for post in page_posts:
    
        #post title
        set_key(df, 'title', post.find('span', attrs = {"class" : "property-card__title js-cardLink js-card-title"}).text.strip())
        
        #post address
        set_key(df, 'address', post.find('span', attrs = {"class" : "property-card__address"}).text.strip())
        
        #post size in m2
        set_key(df, 'area', post.find('span', attrs = {"class" : "property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area"}).text.strip())
        
        #post bathrooms
        set_key(df, 'bathrooms', post.find('li', attrs = {"class" : "property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom"}).text.split()[0])
        
        #post bedrooms
        set_key(df, 'bedrooms', post.find('li', attrs = {"class" : "property-card__detail-item property-card__detail-room js-property-detail-rooms"}).text.split()[0])
        
        #post parking spots
        set_key(df, 'parking_spots', post.find('li', attrs = {"class" : "property-card__detail-item property-card__detail-garage js-property-detail-garages"}).text.split()[0])
        
        #get extra contents
        if post.find('ul', attrs = {"class" : "property-card__amenities"}):
            set_key(df, 'extra_contents',[elem.text for elem in post.find('ul', attrs = {"class" : "property-card__amenities"}).find_all('li')])
        else:
             set_key(df, 'extra_contents', None)
            
        #post property rent
        set_key(df, 'rent', post.find('p', attrs = {"style" : "display: block;"}).text.split()[1])
        
        #post condominium fee
        if post.find('strong', attrs = {"class" : "js-condo-price"}):
           set_key(df, 'fee', post.find('strong', attrs = {"class" : "js-condo-price"}).text)
        else:
            set_key(df, 'fee', None)
        
        post_num += 1
                                            
    page += 1
    print("page", page, "scraped!")
    
    #ckick on next page
    element = driver.find_element_by_partial_link_text('Próxima')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(5)

driver.quit()
    
#making dict into dataframe
df = pd.DataFrame.from_dict(df, orient = 'index').transpose()
df.to_csv('scraped_df.csv', index = False)

