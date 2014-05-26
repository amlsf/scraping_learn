#TODO Did Matthew want me to write my scraper in Morph.io??

from bs4 import BeautifulSoup
# TODO which of these 3 is better?
import requests
import urllib2
import scraperwiki
import re
import sys

# TODO how do I scrape through multiple pages?
def create_url():
    keyword = raw_input("Enter keyword to search: ")
    location = raw_input("Enter address, zipcode, or neighborhood: ")

    url = ""

    return url

def create_soup(url):

    html = urllib2.urlopen(url).read()
    # method #2: trying out scraperwiki library
    # html = scraperwiki.scrape(url)

    soup = BeautifulSoup(html)

    print soup.prettify().encode('utf-8')
    # return soup

    listings = soup.select()




def get_business_name():
    pass

def get_business_address():
    pass

def get_business_phone():
    pass


# TODO: For extra credit, transform the results into  vCard entries (your choice of version). You can check their validity by clicking on them once and pressing spacebar in Finder (or control-click and choose Quick Look if you prefer the mouse).
def create_vcard():
    pass
    # segment = {
    # 'episode_date': episode_date,
    # 'episode_order': idx,
    # 'artists': u'\n'.join(artists),
    # 'pid': segment_pid,
    # 'episode_pid': pid,
    # 'track_title': title,
    # 'record_name': record_name,
    # 'track_num': track_num,
    # 'track_label': label,
    # }
    # yield segment

    # rows = []
    # for u in get_episodes():
    #     for row in get_listings(u):
    #         rows.append(row)
    # #NOTE: This is writing out to the sqlite database using scraperwiki library
    # scraperwiki.sqlite.save(unique_keys=['episode_pid', 'pid'], data=rows)


# TODO try out Scrapy for execution methods
def main():
    create_soup("http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes")

if __name__ == "__main__":
    main()



# Instructions from morph.io

# This is a template for a Python scraper on Morph (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries. You can use whatever libraries are installed
# on Morph for Python (https://github.com/openaustralia/morph-docker-python/blob/master/pip_requirements.txt) and all that matters
# is that your final data is written to an Sqlite database called data.sqlite in the current working directory which
# has at least a table called data.