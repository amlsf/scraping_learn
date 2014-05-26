# Experimenting with examples from http://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/

from bs4 import BeautifulSoup
import requests
import urllib2

def find_all_requests():
    url = raw_input("Enter a website: ")

    # use requests library to get content and read
    r = requests.get("http://" + url)
    data = r.text

    # create soup object
    soup = BeautifulSoup(data)

    # extract all urls within page's 'a' tags. find_all returns list of elements with tag "a". Then .get like dictionary where key is 'href' and value is URL
    # for link in soup.find_all('a'):
    #     print(link.get('href'))

    # get all the text from page
    print(soup.get_text)

    # print soup.a

def prettify_urllib():
    url = "http://www.pythonforbeginners.com"

    # use urllib2 library to get content and read
    content = urllib2.urlopen(url).read()

    # create soup object
    soup = BeautifulSoup(content)

    print soup.prettify().encode('utf-8')

    print soup.title
        # prints <title> Pythonforbeginners.com - Learn Python by Example </title>

    print soup.title.string
        # prints <title> Pythonforbeginners.com - Learn Python by Example </title>

    print soup.p
        # prints None

    print soup.a
        # prints:
        # <a class="navbar-brand" href="/" title="pythonforbeginners.com">
        # <span class="first-part">python</span> for beginners
        #           <!-- <img src="http://s.pythonforbeginners.com/static/img/logo.png" alt="pythonforbeginners.com">-->
        # </a>



def main():
    # find_all_requests()
    prettify_urllib()

if __name__ == "__main__":
    main()