'''
Script to scrape the top posts and comments data from /r/india.
'''
import time
import csv
import praw


def authenticate():
    '''Authenticates the user based on the .ini file.'''
    print('Authenticating...')
    reddit = praw.Reddit(
        'WebMiningProject', user_agent='web:web-mining-project-bot:v0.1 (by /u/pranau97)')
    print('Authenticated as /u/{}'.format(reddit.user.me()))
    return reddit


def get_posts(reddit):
    '''Fetches the top 1000 posts from http://reddit.com/r/india of the past year.'''

    with open(r"out/dataset.csv", "a") as outfile:
        for submission in reddit.subreddit('india').top('year', limit=1000):
            print(submission.title)
            data = [
                submission.title,
                submission.author,
                submission.created_utc,
                submission.score,
                submission.link_flair_text,
                submission.domain,
                "%r" % submission.selftext,
                submission.id
            ]
            writer = csv.writer(outfile)
            writer.writerow(data)
            time.sleep(1)


def get_comments(reddit):
    '''Gets the top 100 comments of each top 1000 post of http://reddit.com/r/india.'''

    with open(r"out/dataset.csv", "r") as infile:
        reader = csv.reader(infile)

        resume_flag = 0

        for row in reader:
            post_id = str(row[7])

            if post_id == "6am00f":
                resume_flag = 1
            if not resume_flag:
                continue

            submission = reddit.submission(id=post_id)
            submission.comments.replace_more(limit=30, threshold=10)

            comment_count = 0

            for comment in submission.comments.list():
                if comment_count >= 100:
                    break

                if isinstance(comment, praw.models.MoreComments):
                    comment_count += 1
                    continue

                comment_str = comment.body
                comment_count += 1

                if comment_str == "[deleted]" or comment_str == "[removed]":
                    continue

                with open(r"out/dataset_comments.csv", "a") as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(["%r" % comment_str, post_id])

            print("Finished post:", post_id)
            time.sleep(2)


def main():
    '''The main function that calls the other functions.'''
    reddit = authenticate()
    get_posts(reddit)
    get_comments(reddit)


if __name__ == '__main__':
    main()
