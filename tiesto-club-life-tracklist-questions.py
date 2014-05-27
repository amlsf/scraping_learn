# TODO what is this for?
# -*- coding: utf-8 -*-

# NOTE: lots of "defensive coding" in here.
# NOTE: anything marked "NOTE" is Amy's note to self
# NOTE: TODO are questions

# TODO what is this import __future__?
from __future__ import print_function
import re
import sys
# TODO: what is scraperwiki? just alternative to urllib2 and requests? Google says some sort of paid service? I pip installed it: "Successfully installed scraperwiki dumptruck"
import scraperwiki
from datetime import datetime
from bs4 import BeautifulSoup

def get_episode_links():
    html = scraperwiki.scrape('http://www.tiestoblog.com/tiesto-club-life/')
    soup = BeautifulSoup(html)
    # NOTE every episode is enclosed in an <article> tag that has this itemtype
    #TODO What's the difference between find_all and select?
    # TODO is there a faster way to find unique patterns faster than trying to sift through "View Source" & inspector?
    postings = soup.select('[itemtype="http://schema.org/BlogPosting"]')
    for p in postings:
        # NOTE every episode has an A tag with rel "bookmark" in it
        bk_a_list = p.select('a[rel=bookmark]')
        if not bk_a_list:
            # TODO what is repr() and file=sys.stderr?
            print('Unable to find rel=bookmark in %s' % repr(p), file=sys.stderr)
            continue
        # NOTE Removing item from list form? only one item in list
        bk_a = bk_a_list[0]
        #NOTE check what attrs does. attrs creates dictionary
        item_href = bk_a.attrs.get('href')
        if not item_href:
            print('Odd, a@rel=bookmark had no href %s' % repr(bk_a), file=sys.stderr)
            continue
        # NOTE: Regex checking to make sure it follows the convention of episode href, e.g. "/tiesto-club-life-367/"
        if re.search(r'life-\d+/$', item_href):
            # NOTE stores link in generator
            # TODO benefit of yield over append and return a list here to manage memory?
            yield item_href
        else:
            print('Skipping unexpected href: %s' % repr(item_href), file=sys.stderr)


def get_episode_bodies():
    # pull each link for each item
    for url in get_episode_links():
        html = scraperwiki.scrape(url)
        soup = BeautifulSoup(html)
        entries = soup.select('[itemtype="http://schema.org/BlogPosting"]')
        if not entries:
            print('No blog postings on %s' % repr(url), file=sys.stderr)
            continue
        posting = entries[0]
        bodies = posting.select('[itemprop=articleBody]')
        if not bodies:
            print('Unable to find articleBody in %s' % repr(posting), file=sys.stderr)
            continue
        body = bodies[0]
        ma = re.search(r'life-(\d+)/$', url)
        if not ma:
            print('Odd URL you have there "%s"' % repr(url), file=sys.stderr)
            episode = 0
        else:
            # TODO what does .group(1) do?
            episode = int(ma.group(1))
        # all that getattr jazz is because NavigableString has no 'name'
        # TODO how is this concatenating the body contents? What is this concatenating? what is "it" and "ii"? what is this doing with unicode and u''? Look up gettattr and startswith(). Syntax is different with the if else statements (like list comprehensions?) why starts with 'h'?
        payload = u''.join([u'\n%s\n ' % it.text if getattr(it, 'name', '').startswith('h')
                            else u''.join(['\n' if getattr(ii, 'name', '') == 'br' else unicode(ii)
                                           for ii in it.contents])
                            for it in body.contents])
        payload = payload.strip()
        # sqlite prefers unicode, so don't encode the str
        output = {
            'episode': episode,
            'text': payload,
            'url': url,
        }
        yield output


def main():
    # careful, .weekday() is Monday indexed so Sun = 6
    #if 6 != datetime.utcnow().weekday():
    #    return 0
    # NOTE: puts all the items in get_episode_bodies generator into data_items and puts in sqlite database.
    data_items = list(get_episode_bodies())
    # episode# may be a better key

    # TODO Why does traditional syntax "print data_items" not work?
    print(data_items)

    # Write out to the sqlite database using scraperwiki library
    # scraperwiki.sqlite.save(unique_keys=['url'], data=data_items)


if __name__ == '__main__':
    main()



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