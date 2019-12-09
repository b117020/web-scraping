# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:52:49 2019

@author: Devdarshan
"""
#import necessary modules
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import re

#load driver to use chrome
driver = webdriver.Chrome("C://Users//Devdarshan//Downloads//chromedriver_win32//chromedriver.exe")

blog_title = []
blog_link = []
blog_content = []
questions = [] 
sub_headings = []
hyperlinks = []


#Scraping from https://www.python-course.eu/machine_learning.php


url = 'https://www.python-course.eu/machine_learning.php'
urlopen = urllib.request.urlopen(url)
soup =BeautifulSoup(urlopen,'html.parser')


#scrape blog title
for a in soup.find_all('div', {'class' : 'menu'}, limit = 10):
    for i in a.find_all('li', limit = 10):
        content=i.find('a').text
        blog_title.append(content)
  
#scrape blog link

for a in soup.find_all('div', {'class' : 'menu'}, limit = 10):
    for i in a.find_all('li', limit = 10):
        content=i.a['href']
        blog_link.append("https://www.python-course.eu/"+content)

#scrape blog content and sub headings

for i in range(0,10):
    temp = " "
    head = " "
    url = blog_link[i]
    urlopen = urllib.request.urlopen(url)
    soup =BeautifulSoup(urlopen,'html.parser')
    for a in soup.find_all('div', {'class' : 'cell border-box-sizing text_cell rendered'}):
        for i in a.find_all('div', {'class' : 'inner_cell'}):
            heading=i.h3
            para = i.find('p')
            head=  head +str(heading)+","
            temp= temp + str(para)
    #blog_content.append(temp)
    sub_headings.append(head)
    
    
    
import requests
for i in range(0,10):
    url = blog_link[i]
    res = requests.get(url)
    html_page = res.content


    soup = BeautifulSoup(html_page, 'html.parser')

    text = soup.find_all(text=True)
    set([t.parent.name for t in text])

    output = ''
    blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
    'style',
    '[document]',
 
	# there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    blog_content.append(output)
#scrape hyperlinks
for i in range(0,10):
    links = " "
    url = blog_link[i]
    urlopen = urllib.request.urlopen(url)
    soup =BeautifulSoup(urlopen,'html.parser')
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        content = link.get('href')
        links=  links +"https://www.python-course.eu/"+str(content)
        
    hyperlinks.append(links)
    


#Scraping from https://www.hackerearth.com/blog/machine-learning/



url = 'https://www.hackerearth.com/blog/machine-learning/'
urlopen = urllib.request.urlopen(url)
soup =BeautifulSoup(urlopen,'html.parser')

#scrape blog title
for a in soup.find_all('div', {'class' : 'content-block'}, limit = 10):
    for i in a.find_all('h3', limit = 10):
        content=i.find('a').text
        blog_title.append(content)
  
#scrape blog links
for a in soup.find_all('div', {'class' : 'content-block'}, limit = 10):
    for i in a.find_all('h3', limit = 10):
        content=i.a['href']
        blog_link.append(content)
        
#scrape blog content and sub headings
for i in range(10,20):
    temp = " "
    head = " "
    url = blog_link[i]
    urlopen = urllib.request.urlopen(url)
    soup =BeautifulSoup(urlopen,'html.parser')
    for a in soup.find_all('div',{'class' : 'entry-content'}):
        for k in a.find_all('h2'):
            try:
                heading=k.b
            except TypeError:
                heading=k.strong
            head=  head +str(heading)+","
        for i in a.find_all('p'):
            para = i.find('span')
            temp= temp + str(para)
    #blog_content.append(temp)
    sub_headings.append(head)


import requests
for i in range(10,20):
    url = blog_link[i]
    res = requests.get(url)
    html_page = res.content


    soup = BeautifulSoup(html_page, 'html.parser')

    text = soup.find_all(text=True)
    set([t.parent.name for t in text])

    output = ''
    blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
    'style',
	'script',
    '[document]',
 
	# there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    blog_content.append(output)
#scrape hyperlinks
for i in range(10,20):
    links = " "
    url = blog_link[i]
    urlopen = urllib.request.urlopen(url)
    soup =BeautifulSoup(urlopen,'html.parser')
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        content = link.get('href')
        links=  links +str(content)
        
    hyperlinks.append(links)


#clean dirty data
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)
for i in range(0,20):
    blog_content[i]=remove_tags(blog_content[i])
    sub_headings[i]=remove_tags(sub_headings[i])
blog_content= remove_tags(str(blog_content)).tolist()



#convert the lists into a dataframe merging them together
df = pd.DataFrame({'Blog Title':blog_title,'Blog Link':blog_link,'Blog Content':blog_content,'Sub Headings':sub_headings,'Hyperlinks':hyperlinks}) 

#dataframe to csv
df.to_csv('D:\web-scraping\cscrape.csv',index = True)














