from requests import get
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

# Copy and replace the url of your craigslist favorite list here
fav_url='https://minneapolis.craigslist.org/favorites?fl=aXRlbXM6NzE4NTI0MDA4NSwzNzIyMzU4LDUxMjUzMDUsNTE4NTk1Myw1NDcyNTk0LDU1ODk1MTMsNjc4OTM3NSw3MjU3ODM1LDgwODk3NDYsOTYxNTI2OCw5ODU1Mjk2LDEyMDg5Mzk3LDEyNDM2ODU0LDEyNjQzNDkyLDEyNjY3ODI5LDEyNjk1OTI0LDEzMTIzNjM2LDEzNDY1MjU0LDEzNzY1ODA4LDEzODM5NzM0LDE0NTA2MTU3LDE1ODQwMTA5LDE1OTM5NjkyLDE2ODE2Mjg5LDE2OTEzNzUzLDE3MTk3NTE4'


response = get(fav_url)
html_soup = BeautifulSoup(response.text, 'html.parser')
posts = html_soup.find_all('li', class_= 'result-row')

post_timing = []
post_hoods = []
post_title_texts = []
cylinders = []
drive = []
post_links = []
post_prices = []
condition = []
fuel=[]
odometer=[]
color=[]
size=[]
title=[]
transmission=[]
bodytype = []
vin=[]
car=[]


#define the posts
posts = html_soup.find_all('li', class_= 'result-row')

#extract data item-wise
for post in posts:

    if post.find('span', class_ = 'result-hood') is not None:

        #posting date
        #grab the datetime element 0 for date and 1 for time
        post_datetime = post.find('time', class_= 'result-date')['datetime']
        post_timing.append(post_datetime)

        #neighborhoods
        post_hood = post.find('span', class_= 'result-hood').text
        post_hoods.append(post_hood)

        #title text
        post_title = post.find('a', class_='result-title hdrlnk')
        post_title_text = post_title.text
        post_title_texts.append(post_title_text)

        #post link
        post_link = post_title['href']
        post_links.append(post_link)

        #removes the \n whitespace from each side, removes the currency symbol, and turns it into an int
        post_price = int(post.a.text.strip().replace("$", ""))
        post_prices.append(post_price)

        #get car's attribute from car's link

        response_car = get(post_link)
        car_soup = BeautifulSoup(response_car.text, 'html.parser')

        car.append(car_soup.find_all('p', class_= 'attrgroup')[0].text.strip())

        car_info = car_soup.find_all('p', class_= 'attrgroup')[1]

        car_attr = defaultdict(lambda: np.nan)
        for attr in car_info.find_all('span'):
            car_attr[attr.text.strip().split(': ')[0]]=  attr.text.strip().split(': ')[1]

        condition.append(car_attr['condition'])
        cylinders.append(car_attr['cylinders'])
        drive.append(car_attr['drive'])
        size.append(car_attr['size'])
        fuel.append(car_attr['fuel'])
        odometer.append(car_attr['odometer'])
        color.append(car_attr['paint color'])
        title.append(car_attr['title status'])
        transmission.append(car_attr['transmission'])
        bodytype.append(car_attr['type'])
        vin.append(car_attr['VIN'])


iterations += 1

print("Page " + str(iterations) + " scraped successfully!")


df_fav_car = pd.DataFrame({'post_timing': post_timing,
 'post_hoods': post_hoods,
 'post_title': post_title_texts,
 'post_links':post_links,
 'car':car,
 'price':post_prices,
 'odometer':odometer,
 'cylinders':cylinders,
 'transmission':transmission,
 'drive':drive,
 'bodytype':bodytype,
 'fuel':fuel,
 'condition':condition,
 'color':color,
 'size':size,
 'title':title,
 'vin':vin
})


df_fav_car['cylinders'] = df_fav_car['cylinders'].str.split().str[0]


df_fav_car.to_csv('fav_used_car.csv', index=False)

print("\n")

print("Scrape complete!")
