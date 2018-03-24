import requests
from bs4 import BeautifulSoup
import os, errno
import csv

filename = 'Table_Allmovie.csv'
dataitem_list = ['Title', "Certificate", "Genre", "Rating", "Running Time", "Directors", "Writers", "Stars Cast", "Country", "Language", "Budget", "Gross", "Release Date", "Production Company"]

try:
    os.remove(filename)
except OSError:
    pass

with open(filename, 'a') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(dataitem_list)


def extract_source(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=headers).text
    return source

def extract_data(source):
    soup=BeautifulSoup(source, 'lxml')
    return soup


def getlink(num_of_tuples):
    page = 1
    max_page = num_of_tuples/12
    item_num = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    while(page <= max_page):
        url = 'https://www.allmovie.com/genre/drama-d649/alltime-desc/' + str(page)
        #url = 'https://www.allmovie.com/genre/war-d947/alltime-desc/' + str(page)
        #url = 'https://www.allmovie.com/genre/action-d646/alltime-desc/' + str(page)
        #url = 'https://www.allmovie.com/genre/thriller-d942/alltime-desc/' + str(page)
        #url = 'https://www.allmovie.com/genre/crime-d653/alltime-desc/' + str(page)
        html_source = requests.get(url, headers=headers)
        plain_html = html_source.text
        soup = BeautifulSoup(plain_html.encode('ascii', 'ignore'), "html.parser")
        for link in soup.findAll('div', {'class': 'movie_row'}):
            for link1 in link.findAll('div'):
                for link2 in link1.findAll('p', {'class': 'title'}):
                    item_url = 'https://www.allmovie.com' + link2.find('a').get('href') + '/cast-crew'
                    item_num += 1
                    getdata(item_url,item_num)
        page += 1

def getdata(i_url, i_num):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        dataitem_list = []
        print "ITEM NUM:" + str(i_num)
        item_html_source = requests.get(i_url, headers=headers)
        item_plain_html = item_html_source.text
        soup = BeautifulSoup(item_plain_html.encode('ascii', 'ignore'), "html.parser")

        #Title
        item_title = "NULL"
        for link in soup.findAll('h2', {'class': 'movie-title'}):
            item_title = link.contents[0].strip()
            item_title = "".join(item_title).encode('utf-8').strip()
            print item_title

        #Certificate
        item_certi = "NULL"
        for link in soup.findAll('div', {'class': 'mpaa'}):
            item_certi = link.find('div')
            item_certi = "".join(item_certi).encode('utf-8').strip()
            #print item_certi

        #Genre
        item_genre = []
        for link in soup.findAll('span', {'class': 'header-movie-genres'}):
            for link1 in link.findAll('a'):
                item_genre.append(link1.string)
            item_genre = "|".join(item_genre).encode('utf-8').strip()
        #print item_genre


        #Rating
        item_rating = "NULL"
        for link in soup.findAll('div', {'itemprop': 'ratingValue'}):
            item_rating = link.string.strip()
            item_rating = "".join(item_rating).encode('utf-8').strip()
            #print item_rating

        #running_time
        item_running_time = "NULL"
        item_release = "NULL"
        item_country = []
        link = soup.find('hgroup', {'class': 'details'})
        if(link):
            for link1 in link.findAll('span'):
                detail = link1.contents[0].strip()
                if(detail=='Run Time -'):
                    item_running_time = link1.find('span').string.strip()
                    item_running_time = "".join(item_running_time).encode('utf-8').strip()
                    #print item_running_time
                elif(detail=='Countries -'):
                    item_country = link1.find('span').string.strip().split(", ")
                    item_country = "|".join(item_country).encode('utf-8').strip()
                    #print item_country
                elif(detail=='Release Date -'):
                    item_release = link1.find('span').string.strip()
                    item_release = "".join(item_release).encode('utf-8').strip()
                    #print item_release

        #Directors
        item_directors = []
        for link in soup.findAll('h3', {'class': 'movie-director'}):
            for link1 in link.findAll('span', {'itemprop': 'name'}):
                for link2 in link1.findAll('a'):
                    item_directors.append(link2.string.strip())
                item_directors = "|".join(item_directors).encode('utf-8').strip()
        #print item_directors


        #Start Cast
        item_stars = []
        for link in soup.findAll('div', {'class': 'cast_name artist-name'}):
            for link1 in link.findAll('a'):
                item_stars.append(link1.contents[0])
        del item_stars[4:]
        item_stars = "|".join(item_stars).encode('utf-8').strip()
        #print item_stars


        #Production Company
        item_production = []
        for link in soup.findAll('div', {'class': 'produced-by'}):
            item_production = link.find('div').string.strip().split(", ")
        item_production = "|".join(item_production).encode('utf-8').strip()
        #print item_production


        item_writers = []
        item_language = []
        item_budget = "NULL"
        item_gross = "NULL"

        dataitem_list.append(item_title.strip())
        dataitem_list.append(item_certi.strip())
        if not item_genre:
            dataitem_list.append("NULL")
        else:
            dataitem_list.append(item_genre)
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

getlink(3000)
