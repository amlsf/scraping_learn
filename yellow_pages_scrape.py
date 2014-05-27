#TODO Did Matthew want me to write my scraper in Morph.io??
#TODO do I need to have any regex checks?
#TODO is the coding defensive enough?
# TODO should I use yield instead of return?

# TODO what is this utf-8 comment for?
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
# TODO which of these 3 is better?
import requests
import urllib2
import scraperwiki
import re
import sys
import vobject

# TODO how do I scrape through multiple pages? Scrape links to additional pages until no more
# TODO write this function so it does a custom URL
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
    business_name = business_name[0].get_text()
    return business_name

def get_business_phone(listing):
    phone = listing.select('[itemprop="telephone"]')
    if not phone:
        print "no phone"
        phone = ""
    phone = phone[0].get_text()
    return phone

def get_business_address(listing):
    # get street address
    street_address = listing.select('[itemprop="streetAddress"]')
    if not street_address:
        print "no street address"
        street_address = ""
    street_address = street_address[0].get_text()

    # get city
    locality = listing.select('[itemprop="addressLocality"]')
    if not locality:
        print "no address locality"
        locality = ""
    locality = locality[0].get_text()

    # get state
    region = listing.select('[itemprop="addressRegion"]')
    if not region:
        print "no address region"
        region = ""
    region = region[0].get_text()

    # get postal code
    postal_code = listing.select('[itemprop="postalCode"]')
    if not postal_code:
        print "no postal code"
        postal_code = ""
    postal_code = postal_code[0].get_text()

    return {'street_address': street_address, 'locality': locality, 'region': region, 'postal_code': postal_code}


# TODO: [What does this last part mean - is this mac specific?] "For extra credit, transform the results into  vCard entries (your choice of version). You can check their validity by clicking on them once and pressing spacebar in Finder (or control-click and choose Quick Look if you prefer the mouse)"
# TODO how to get items to order?
# TODO How do I create the vcard .vcf and export?
def create_vcard(business_name, business_phone, business_address):
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

    # TODO better to use yield?
    return j.serialize()

# TODO try out Scrapy for execution methods
def main():
    # url = create_url()
    # create_soup(url)
    create_soup("http://www.yellowpages.com/tucson-az/cupcakes?g=tucson%2C%20az&q=cupcakes")
    # create_vcard()

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