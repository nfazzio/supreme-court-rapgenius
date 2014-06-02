import urllib2
from contextlib import closing
from bs4 import BeautifulSoup

def main():
    cases = get_cases()

def get_cases():
    url = 'http://en.wikipedia.org/wiki/List_of_United_States_Supreme_Court_cases'
    with closing(urllib2.urlopen(url)) as page:
        soup = BeautifulSoup(page)
        print soup
        print soup.prettify()

if __name__ == "__main__":
    main()
