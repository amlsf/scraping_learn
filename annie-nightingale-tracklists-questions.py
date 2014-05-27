# -*- coding: utf-8 -*-

# NOTE: lots of "defensive coding" in here.
# NOTE: anything marked "NOTE" is Amy's note to self
# NOTE: TODO are questions

from __future__ import print_function
import re
import sys
# TODO: why not using urllib2?
import urllib
import scraperwiki
from datetime import datetime
from bs4 import BeautifulSoup

#NOTE this returns a generator of episode links
def get_episodes():
    broadcasts_url = 'http://www.bbc.co.uk/programmes/b006wkp7/broadcasts'
    html = scraperwiki.scrape(broadcasts_url)
    soup = BeautifulSoup(html)

    episodes = soup.select('[typeof="po:Episode"]')
    for epi in episodes:
        titles = epi.select('[property="dc:title"]')
        #NOTE if there's nothing in titles, then continue on in next for loop iteration?
        if not titles:
            continue
        title = titles[0]
        # this one is a *future* episode, it has not yet been titled
        #TODO is this checking and skipping something related to being a future episode? marked as a digit? why the "r'" in front?
        if re.match(r'\d\d/\d\d/\d\d\d\d', title.text):
            continue
        parent_a = title.parent
        #TODO check what getattr() does
        if 'a' != getattr(parent_a, 'name', ''):
            # TODO not sure what this is doing with repr and sys.stderr (checking for parent of A)
            print('Odd, dc:title has no A parent: %s' % repr(title), file=sys.stderr)
            continue
        #NOTE: get all the links from A parent of episode
        epi_href = parent_a.attrs.get('href')
        #NOTE: if not href link
        if not epi_href:
            print('Odd, dc:title A has no href: %s' % repr(title), file=sys.stderr)
            continue
        #NOTE yield is generator, referenced in main() function
        #TODO what is .basejoin? taking url and episode href referenced in A tag parent of episode
        yield urllib.basejoin(broadcasts_url, epi_href)

#NOTE This passes in episode url yielded from get_episodes()
def get_listings(url):
    html = scraperwiki.scrape(url)
    #TODO check regex for this pattern matching; it's checking for a certain URL format (see else stmt below)
    pid_ma = re.search(r'/programmes/([^/]+)$', url)
    if pid_ma:
        # TODO I think .group(1) is taking just the first item?
        pid = pid_ma.group(1)
    else:
        print('Whoa, bogus URL format you have there: %s' % repr(url), file=sys.stderr)
        pid = url  # *shrug* but pid is the primary key, so it has to be something
    soup = BeautifulSoup(html)
    #NOTE Pulling out all the broadcast types
    broadcasts = soup.select('[typeof="po:Broadcast"]')
    #TODO what's a crummy? Elaborate on this comment. Is this episode_date to instantiate?
    # pick a crummy, but non-None default
    episode_date = datetime.utcnow().isoformat(' ').split(' ')[0]
    if broadcasts:
        broad = broadcasts[0]
        tl_starts = broad.select('[property="timeline:start"]')
        if tl_starts:
            tl_start = tl_starts[0]
            # e.g. "2014-04-19T03:00:00+01:00"
            episode_dt = tl_start.attrs.get('content', '')
            if episode_dt:
                ma = re.match(r'(\d{4}-\d{2}-\d{2})', episode_dt)
                if ma:
                    episode_date = ma.group(1)
                else:
                    print('Unable to match your episode date: %s' % repr(episode_dt), file=sys.stderr)
            else:
                print('Odd, your timeline start has no @content: %s' % repr(tl_start), file=sys.stderr)
        else:
            print('Unable to find :start in :Broadcast\n%s' % repr(broad), file=sys.stderr)
    else:
        print('Unable to find :Broadcast, so no d/t for you', file=sys.stderr)

    tracks = soup.select('[typeof="po:MusicSegment"]')
    for idx, t in enumerate(tracks):
        about_segment = t.attrs.get('about')
        if about_segment:
            segment_pid_ma = re.search(r'/programmes/([^/#]+)', about_segment)
            segment_pid = segment_pid_ma.group(1)
        else:
            print('Egad, segment has no @about\n%s' % repr(t), file=sys.stderr)
            segment_pid = '%s-number-%d' % (pid, idx)
        performers = t.select('[typeof="mo:MusicArtist"]')
        artists = []
        for p in performers:
            if p.attrs.get('property', '') == 'foaf:name':
                name = p.text
            else:
                names = p.select('[property="foaf:name"]')
                if not names:
                    print('An artist without a name?\n%s' % repr(p), file=sys.stderr)
                    continue
                name = names[0].text
                del names
            artists.append(name)
            del name
        # have to h3 qualify this because there is dc:title for the Record, too
        title_el = t.select('h3 [property="dc:title"]')
        if title_el:
            title = title_el[0].text
        else:
            title = 'Untitled'  # *shrug*
        record_name = ''
        record_el = t.select('[typeof="mo:Record"]')
        if record_el:
            rec_titles = record_el[0].select('[property="dc:title"]')
            if rec_titles:
                record_name = rec_titles[0].text
            else:
                print('Record with no title?\n%s' % repr(record_el), file=sys.stderr)
        track_el = t.select('.track-number')
        track_num = None
        if track_el:
            try:
                track_num = int(track_el[0].text)
            except ValueError:
                print('Bogus track_number text "%s"' % repr(track_el), file=sys.stderr)
        label_el = t.select('.record-label')
        label = ''
        if label_el:
            label = label_el[0].text
        segment = {
            'episode_date': episode_date,
            'episode_order': idx,
            'artists': u'\n'.join(artists),
            'pid': segment_pid,
            'episode_pid': pid,
            'track_title': title,
            'record_name': record_name,
            'track_num': track_num,
            'track_label': label,
        }
        yield segment


def main():
    # careful: .weekday() is Monday indexed
    #if 5 != datetime.utcnow().weekday():
    #    return 0
    rows = []
    for u in get_episodes():
        for row in get_listings(u):
            rows.append(row)
    # turns out the "pid" is the *track* id, not just the broadcast
    # of that track within an episode
    #NOTE: This is writing out to the sqlite database using scraperwiki library
    scraperwiki.sqlite.save(unique_keys=['episode_pid', 'pid'], data=rows)


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