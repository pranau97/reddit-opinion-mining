'''
A Reddit bot that posts explanation of xkcd comic strips posted in comments
The explanation is extracted from http://explainxkcd.com
License: MIT License
'''
import pprint
import praw

def authenticate():
    '''Authenticates the user based on the .ini file.'''
    print('Authenticating...')
    reddit = praw.Reddit('WebMiningProject', user_agent='web:web-mining-project-bot:v0.1 (by /u/pranau97)')
    print('Authenticated as {}'.format(reddit.user.me()))
    return reddit

def get_posts(reddit):
    '''Fetches the posts from reddit.'''

    for submission in reddit.subreddit('india').top(4limit=250):
        print(submission.title)
        pprint.pprint(vars(submission))

def main():
    '''The main function that calls the others.'''
    reddit = authenticate()
    get_posts(reddit)

if __name__ == '__main__':
    PATH = '/home/pranau/programming/reddit-opinion-mining/commented.txt'
    # Location of file where id's of already visited comments are maintained
    main()
