import requests
from bs4 import BeautifulSoup
import os, errno
import csv

filename = 'Table_IMDB.csv'
dataitem_list = ['Title', "Certificate", "Genre", "Rating", "Running Time", "Directors", "Writers", "Stars Cast", "Country", "Language", "Budget", "Gross", "Release Date", "Production Company"]

try:
    os.remove(filename)
except OSError:
    pass

with open(filename, 'a') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(dataitem_list)

def getlink(num_of_tuples):
    page = 7
    max_page = num_of_tuples/50
    item_num = 0
    while(page <= max_page):
        url = 'https://www.imdb.com/search/title?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=b9121fa8-b7bb-4a3e-8887-%20aab822e0b5a7&pf_rd_r=MY2MNXPADVTG5T9J3Z6X&pf_rd_s=right-%206&pf_rd_t=15506&pf_rd_i=moviemeter&genres=action&explore=title_type,genres&page=' + str(page)
        html_source = requests.get(url)
        plain_html = html_source.text
        soup = BeautifulSoup(plain_html, "html.parser")
        for link in soup.findAll('h3', {'class': 'lister-item-header'}):
            item_url = "https://www.imdb.com" + link.find('a').get('href')
            item_name = "https://www.imdb.com" + link.find('a').string
            #print item_name
            item_num += 1
            getdata(item_url,item_num)
        page += 1

def getdata(i_url, i_num):
        dataitem_list = []
        print "ITEM NUM:" + str(i_num)
        item_html_source = requests.get(i_url)
        item_plain_html = item_html_source.text
        soup = BeautifulSoup(item_plain_html, "html.parser")

        #Title
        item_title = "NULL"
        for link in soup.findAll('div', {'class': 'title_wrapper'}):
            item_title = link.find('h1').contents[0].strip()
            item_title = "".join(item_title).encode('utf-8').strip()
            #print item_title

        #Certificate
        item_certi = "NULL"
        for link in soup.findAll('meta', {'itemprop': 'contentRating'}):
            item_certi = link.get('content').strip()
            item_certi = "".join(item_certi).encode('utf-8').strip()
            #print item_certi

        #Genre
        item_genre = []
        for link in soup.findAll('span', {'itemprop': 'genre'}):
            item_genre.append(link.string.strip())
        item_genre = "|".join(item_genre).encode('utf-8').strip()
        #print item_genre


        #Rating
        item_rating = "NULL"
        for link in soup.findAll('span', {'itemprop': 'ratingValue'}):
            item_rating = link.string.strip()
            item_rating = "".join(item_rating).encode('utf-8').strip()
            #print item_rating

        #running_time
        item_running_time = "NULL"
        if(soup.find('time', {'itemprop': 'duration'})):
            item_running_time = soup.find('time', {'itemprop': 'duration'}).string.strip()
            item_running_time = "".join(item_running_time).encode('utf-8').strip()
            #print item_running_time

        #Directors || Writers || Stars
        item_directors = []
        item_writers = []
        item_stars = []
        for link in soup.findAll('div', {'class': 'credit_summary_item'}):
            if(link.find('h4')):
                people = link.find('h4').string
                if(people=="Director:"):
                    item_directors.append(link.find('span', {'itemprop': 'director'}).find('a').string.strip())
                    item_directors = "".join(item_directors).encode('utf-8').strip()
                    #print item_director
                elif(people=="Directors:"):
                    for link1 in link.findAll('span', {'itemprop': 'director'}):
                        item_directors.append(link1.find('a').string.strip())
                    item_directors = "|".join(item_directors).encode('utf-8').strip()
                        #print item_directors
                elif(people=="Writer:"):
                    item_writers.append(link.find('span', {'itemprop': 'creator'}).find('a').string.strip())
                    item_writers = "".join(item_writers).encode('utf-8').strip()
                    #print item_writers
                elif(people=="Writers:"):
                    for link1 in link.findAll('span', {'itemprop': 'creator'}):
                        item_writers.append(link1.find('a').string.strip())
                    item_writers = "|".join(item_writers).encode('utf-8').strip()
                        #print item_writers
                elif(people=="Star:"):
                    item_stars.append(link.find('span', {'itemprop': 'actors'}).find('a').string.strip())
                    item_stars = "".join(item_stars).encode('utf-8').strip()
                    #print item_stars
                elif(people=="Stars:"):
                    for link1 in link.findAll('span', {'itemprop': 'actors'}):
                        item_stars.append(link1.find('a').string.strip())
                    item_stars = "|".join(item_stars).encode('utf-8').strip()
                        #print item_stars

        #Country || Language || Budget || Gross || Release Date || Production CO
        item_country = []
        item_language = []
        item_budget = "NULL"
        item_gross = "NULL"
        item_release = "NULL"
        item_production = []
        for link in soup.findAll('div', {'class': 'txt-block'}):
            if(link.find('h4')):
                text = link.find('h4').string
                if(text=="Country:"):
                    for link1 in link.findAll('a'):
                        item_country.append(link.find('a').string.strip())
                    item_country = "|".join(item_country).encode('utf-8').strip()
                        #print item_country
                elif(text=="Language:"):
                    for link1 in link.findAll('a'):
                        item_language.append(link1.string.strip())
                    item_language = "|".join(item_language).encode('utf-8').strip()
                        #print item_language
                elif(text=="Budget:"):
                    item_budget = link.contents[2].strip()
                    item_budget = "".join(item_budget).encode('utf-8').strip()
                    #print item_budget
                elif(text=="Cumulative Worldwide Gross:"):
                    item_gross = link.contents[2].strip()
                    item_gross = "".join(item_gross).encode('utf-8').strip()
                    #print item_gross
                elif(text=="Release Date:"):
                    item_release = link.contents[2].strip()
                    item_release = "".join(item_release).encode('utf-8').strip()
                    #print item_release
                elif(text=="Production Co:"):
                    for link1 in link.findAll('span', {'itemprop': 'creator'}):
                        item_production.append(link1.find('a').string.strip())
                    #print item_production

        item_production = "|".join(item_production).encode('utf-8').strip()
        dataitem_list.append(item_title.strip())
        dataitem_list.append(item_certi.strip())
        dataitem_list.append(item_genre.strip())
        dataitem_list.append(item_rating.strip())
        dataitem_list.append(item_running_time.strip())
        if not item_directors:
            dataitem_list.append("NULL")
        else:
            dataitem_list.append(item_directors)
        if not item_writers:
            dataitem_list.append("NULL")
        else:
            dataitem_list.append(item_writers)
        if not item_stars:
            dataitem_list.append("NULL")
        else:
            dataitem_list.append(item_stars)
        if not item_country:
            dataitem_list.append("NULL")
        else:
            dataitem_list.append(item_country)
        if not item_language:
            dataitem_list.append("NULL")
        else:
            dataitem_list.append(item_language)
        dataitem_list.append(item_budget.strip())
        dataitem_list.append(item_gross.strip())
        dataitem_list.append(item_release.strip())
        if not item_production:
            dataitem_list.append("NULL")
        else:
            dataitem_list.append(item_production)
        print dataitem_list
        with open(filename, 'a') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(dataitem_list)

getlink(4000)
