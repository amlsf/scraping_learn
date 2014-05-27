# TODO Did Matthew want me to write this scraper in Morph.io?
# TODO try out Scrapy for execution method
# TODO incorporate sleep function somewhere
# TODO How do I export the .vcf file and view? (I don't have mac or outlook or any vcard organizer)
# TODO: [What does the last part of this stmt mean - is this mac specific?] "For extra credit, transform the results into  vCard entries (your choice of version). You can check their validity by clicking on them once and pressing spacebar in Finder (or control-click and choose Quick Look if you prefer the mouse)"

# TODO do I need to have any regex checks?
# TODO should I use yield instead of return?
# TODO is the coding defensive enough?

# TODO what is this utf-8 comment for?
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys
import re
import vobject
import string
# TODO which of these 3 below is better?
import requests
import urllib2
import scraperwiki

def create_url():
    keyword = raw_input("Enter keyword to search: ")
    location = raw_input("Enter address, zipcode, or neighborhood: ")

    # remove punctuation
    for c in string.punctuation:
        keyword = keyword.replace(c,"")
    for c in string.punctuation:
        location = location.replace(c,"")

    # separate keywords into list
    keyword = keyword.split()
    location = location.split()

    # create keyword insertions separated by dash
    keyword = "-".join(keyword)
    location = "-".join(location)

    url = "http://www.yellowpages.com/" + location + "/" + keyword
    return url

def get_pagination(url):
    yield url
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)

    # stop when there are no more pages (marked by no more "next rel" in source)
    while soup.select('[rel="next"]'):
        next_page = soup.select('[rel="next"]')
        next_page = next_page[0]
        next_page_href = next_page.attrs.get('href')

        yield next_page_href

        html = urllib2.urlopen(next_page_href).read()
        soup = BeautifulSoup(html)

def create_soup(url):
    html = urllib2.urlopen(url).read()
    # method #2: trying out scraperwiki library
    # html = scraperwiki.scrape(url)

    soup = BeautifulSoup(html)
    # print soup.prettify().encode('utf-8')
    # return soup

    listings = soup.select('[itemtype="http://schema.org/LocalBusiness"]')
    # for listing in listings:
    #         print str(listing) + "\n"
    for listing in listings:
        # TODO put more specific error messages here, try repr() and sys.stderr
        if not listing:
            print "no listing"
            continue

        business_name = get_business_name(listing)
        business_phone = get_business_phone(listing)
        business_address = get_business_address(listing)
        # print business_name
        # print business_phone
        # print business_address
        print create_vcard(business_name, business_phone, business_address)

def get_business_name(listing):
    business_name = listing.select('[itemprop="name"]')
    if not business_name:
        print "no business name"
        business_name = ""
    else:
        business_name = business_name[0].get_text()
    return business_name

def get_business_phone(listing):
    phone = listing.select('[itemprop="telephone"]')
    if not phone:
        print "no phone"
        phone = ""
    else:
        phone = phone[0].get_text()
    return phone

def get_business_address(listing):
    # get street address
    street_address = listing.select('[itemprop="streetAddress"]')
    if not street_address:
        print "no street address"
        street_address = ""
    else:
        street_address = street_address[0].get_text()

    # get city
    locality = listing.select('[itemprop="addressLocality"]')
    if not locality:
        print "no address locality"
        locality = ""
    else:
        locality = locality[0].get_text()

    # get state
    region = listing.select('[itemprop="addressRegion"]')
    if not region:
        print "no address region"
        region = ""
    else:
        region = region[0].get_text()

    # get postal code
    postal_code = listing.select('[itemprop="postalCode"]')
    if not postal_code:
        print "no postal code"
        postal_code = ""
    else:
        postal_code = postal_code[0].get_text()

    return {'street_address': street_address, 'locality': locality, 'region': region, 'postal_code': postal_code}


# TODO how to get items in specific order? Format around city is not quite right: shows up like "Tucson\, ;AZ;"
def create_vcard(business_name, business_phone, business_address):
    # TODO vcards are like sets? (.add)
    j = vobject.vCard()
    o = j.add('fn')
    o.value = business_name

    o = j.add('n')
    o.value = vobject.vcard.Name(family=business_name)

    o = j.add('telephone')
    o.type_param = "work"
    o.value = business_phone

    o = j.add('adr')
    o.value = vobject.vcard.Address(street=business_address['street_address'], city=business_address['locality'], region=business_address['region'], code=business_address['postal_code'])

    return j.serialize()

def main():
    url = create_url()
    for link in get_pagination(url):
        create_soup(link)

if __name__ == "__main__":
    main()


##############################################################################################################
##############################################################################################################

# HW instructions

# For homework, scrape the listings off at least one page, preferably all of them, of the yellowpages. com listings for cupcakes in Tucson, AZ [103 as of this email]. A well written scraper will move itself from page to page until it runs out of pages, and will parameterize the starting URL so I can point it to a city and category of my choosing and still have it produce results [and terminate without error].
#
# TODO elaborate on this. Try using sleep function
# Be careful about any automated request mechanism: it needs to throttle itself to avoid becoming a DoS attack and/or getting banned for being a scraper. Putting in a constant value for  sleep is absolutely fine.
#
# TODO elaborate on what is a fail-fast? http://en.wikipedia.org/wiki/Fail-fast
# At this stage, the output format is not as interesting as the mechanics of getting all of them and completing the run without error. I would prefer skipping over one [or even a whole page] instead of fail-fast.
#
# The world is your oyster as far as execution methods; I will be perfectly happy with just a __main__ launched script, and over the moon if it runs in Scrapy.
#
# For extra credit, transform the results into vCard entries (your choice of version). You can check their validity by clicking on them once and pressing spacebar in Finder (or control-click and choose Quick Look if you prefer the mouse).


##############################################################################################################
##############################################################################################################

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

# TODO what is this? Is this in place of what beautiful soup does?
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