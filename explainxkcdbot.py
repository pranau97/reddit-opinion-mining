'''
A Reddit bot that posts explanation of xkcd comic strips posted in comments
The explanation is extracted from http://explainxkcd.com
License: MIT License
'''
from urllib.parse import urlparse

import time
import re
import requests
import praw

import bs4
from bs4 import BeautifulSoup

def authenticate():
    '''Authenticates the user based on the .ini file.'''
    print('Authenticating...\n')
    reddit = praw.Reddit('WebMiningProject', user_agent='web:web-mining-project-bot:v0.1 (by /u/pranau97)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def fetchdata(url):
    '''Fetches the comments from xkcd.'''
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('p')
    data = ''
    while True:
        if isinstance(tag, bs4.element.Tag):
            if tag.name == 'h2':
                break
            if tag.name == 'h3':
                tag = tag.nextSibling
            else:
                data = data + '\n' + tag.text
                tag = tag.nextSibling
        else:
            tag = tag.nextSibling

    return data


def run_explainbot(reddit):
    '''Fetches the comments from reddit.'''
    print("Getting 250 comments...\n")

    for comment in reddit.subreddit('test').comments(limit=250):
        match = re.findall("[a-z]*[A-Z]*[0-9]*https://www.xkcd.com/[0-9]+", comment.body)
        if match:
            print('Link found in comment with comment ID: ' + comment.id)
            xkcd_url = match[0]
            print('Link: ' + xkcd_url)

            url_obj = urlparse(xkcd_url)
            xkcd_id = int((url_obj.PATH.strip("/")))
            my_url = 'http://www.explainxkcd.com/wiki/index.php/' + str(xkcd_id)

            file_obj_r = open(PATH, 'r')

            try:
                explanation = fetchdata(my_url)
            except:
                print('Exception!!! Possibly incorrect xkcd URL...\n')
                # Typical cause for this will be a URL for an xkcd that does not exist (Example: https://www.xkcd.com/772524318/)
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting explanation\n')
                    comment.reply(explanation)

                    file_obj_r.close()

                    file_obj_w = open(PATH, 'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')

            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)


def main():
    '''The main function that calls the others.'''
    reddit = authenticate()
    while True:
        run_explainbot(reddit)


if __name__ == '__main__':
    PATH = '/home/pranau/programming/reddit-opinion-mining/commented.txt'
    # Location of file where id's of already visited comments are maintained
    main()
