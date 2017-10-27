# An independent program to simply fetch and display explanation of an xkcd comic strip
# The explanation is extracted from http://explainxkcd.com
# Created by Ayush Dwivedi (/u/kindw)
# License: MIT License


import requests
import bs4
from bs4 import BeautifulSoup

xkcd_id = 699
# Replace xkcd_id with the serial number of xkcd you want the explanation for

url = 'http://www.explainxkcd.com/wiki/index.php/' + str(xkcd_id)

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')


def main():
    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if (tag.name == 'h2'):
                break
            if (tag.name == 'h3'):
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling
    print (data)


if __name__ == '__main__':
    main()
