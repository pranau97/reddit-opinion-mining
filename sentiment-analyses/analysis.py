'''
Provides analyses on the collected dataset of posts and comments.
'''

import sys
import csv
import math
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk as nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz


def run_sentiment_analysis():
    '''Reads the posts and comments and performs the analysis.'''
    sia = SIA()

    with open(r"out/dataset.csv", "r") as infile_posts:
        with open(r"out/dataset_comments.csv", "r") as infile_comments:
            post_reader = csv.reader(infile_posts)
            comment_reader = csv.reader(infile_comments)

            row_count = 0
            positive_count = 0
            negative_count = 0
            total_count = 0

            for row in post_reader:
                resultult = sia.polarity_scores(row[0])
                print("Analysing post rows: " + str(row_count + 1), end="\r")
                row_count += 1
                total_count += 1

                if resultult['compound'] > 0.2:
                    with open(r"out/positive_list.txt", "a", encoding="utf-8") as outfile_posts_0:
                        outfile_posts_0.write(row[0] + "\n")
                        positive_count += 1

                elif resultult['compound'] < -0.2:
                    with open(r"out/negative_list.txt", "a", encoding="utf-8") as outfile_posts_1:
                        outfile_posts_1.write(row[0] + "\n")
                        negative_count += 1
            print("\nDone.")

            row_count = 0
            for row in comment_reader:
                resultult = sia.polarity_scores(row[0])
                print("Analysing comment rows: " +
                      str(row_count + 1), end="\r")
                row_count += 1
                total_count += 1

                if resultult['compound'] > 0.2:
                    with open(r"out/positive_list.txt", "a", encoding="utf-8") as outfile_comments_0:
                        outfile_comments_0.write(row[0] + "\n")
                        positive_count += 1

                elif resultult['compound'] < -0.2:
                    with open(r"out/negative_list.txt", "a", encoding="utf-8") as outfile_comments_1:
                        outfile_comments_1.write(row[0] + "\n")
                        negative_count += 1

            print("\nDone.")

            plot_word_types(total_count, negative_count, positive_count)


def plot_word_types(total_count, negative_count, positive_count, string=""):
    '''Given the word counts, this method plots a bar graph of the word types.'''
    y_val = [(total_count - positive_count - negative_count) /
             total_count * 100, negative_count / total_count * 100, positive_count / total_count * 100]
    x_val = [1, 2, 3]
    plt.style.use('ggplot')
    ind = np.arange(len(x_val))
    width = 0.3
    _fig, ax = plt.subplots()
    ax.bar(ind + 0.1, y_val, width, color='green')
    ax.set_xticks(ind + 0.1 + width / 2)
    ax.set_xticklabels(['Neutral', 'Negative', 'Positive'])
    plt.title("Categories Distribution of " + string)
    plt.xlabel("Categories")
    plt.ylabel("Percentage")
    plt.show()


def word_distribution(filename):
    '''Plots words distributions for a given file.'''
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))
    all_words = []

    with open(filename, "r", encoding='utf-8') as f_pos:
        for line in f_pos.readlines():
            words = tokenizer.tokenize(line)
            for w in words:
                if w.lower() not in stop_words and w.lower() != "n":
                    all_words.append(w.lower())
    result = nltk.FreqDist(all_words)
    print(result.most_common(8))

    plt.style.use('ggplot')

    y_val = [x[1] for x in result.most_common(len(all_words))]
    y_final = []
    for i, k, z, t in zip(y_val[0::4], y_val[1::4], y_val[2::4], y_val[3::4]):
        y_final.append(math.log(i + k + z + t))
    x_val = [math.log(i + 1) for i in range(len(y_final))]

    plt.xlabel("Words (Log)")
    plt.ylabel("Frequency (Log)")
    plt.title("Word Frequency Distribution")
    plt.plot(x_val, y_final)
    plt.show()


def run_topical_analysis(string):
    '''Searches for a user given string and performs sentiment analysis for it.'''
    sia = SIA()

    print("Searching for " + string + "...")
    with open(r"out/dataset.csv", "r") as infile_posts:
        with open(r"out/dataset_comments.csv", "r") as infile_comments:
            post_reader = csv.reader(infile_posts)
            comment_reader = csv.reader(infile_comments)

            include_list = []
            positive_count = 0
            negative_count = 0
            total_count = 0

            for row in post_reader:
                print("Analyzing posts and comment rows: " +
                      str(total_count + 1), end="\r")

                match_post_title = fuzz.partial_ratio(string, row[0])
                match_post_flair = fuzz.partial_ratio(string, row[4])
                if row[6] == "''":
                    match_post_selftext = 0
                    if match_post_flair >= 85 or match_post_title >= 85:
                        resultult_0 = sia.polarity_scores(row[0])
                        resultult_1 = None
                        include_list.append(row[7])
                    else:
                        continue
                else:
                    match_post_selftext = fuzz.partial_ratio(string, row[6])
                    if match_post_flair >= 85 or match_post_title >= 85 or match_post_selftext >= 85:
                        resultult_0 = sia.polarity_scores(row[0])
                        resultult_1 = sia.polarity_scores(row[4])
                        include_list.append(row[7])
                    else:
                        continue

                if resultult_0['compound'] > 0.2:
                    with open(r"out/positive_list_" + "%r" % string + r".txt", "a", encoding="utf-8") as outfile_posts:
                        outfile_posts.write(row[0] + "\n")
                        positive_count += 1
                        total_count += 1

                elif resultult_0['compound'] < -0.2:
                    with open(r"out/negative_list_" + "%r" % string + r".txt", "a", encoding="utf-8") as outfile_posts:
                        outfile_posts.write(row[0] + "\n")
                        negative_count += 1
                        total_count += 1

                if resultult_1 is not None:
                    if resultult_1['compound'] > 0.2:
                        with open(r"out/positive_list_" + "%r" % string + r".txt", "a", encoding="utf-8") as outfile_posts:
                            outfile_posts.write(row[0] + "\n")
                            positive_count += 1

                    elif resultult_1['compound'] < -0.2:
                        with open(r"out/negative_list_" + "%r" % string + r".txt", "a", encoding="utf-8") as outfile_posts:
                            outfile_posts.write(row[0] + "\n")
                            negative_count += 1

            for row in comment_reader:
                print("Analyzing posts and comment rows: " +
                      str(total_count + 1), end="\r")

                if row[1] in include_list:
                    total_count += 1

                    resultult = sia.polarity_scores(row[0])

                    if resultult['compound'] > 0.2:
                        with open(r"out/positive_list_" + "%r" % string + r".txt", "a", encoding="utf-8") as outfile_comments:
                            outfile_comments.write(row[0] + "\n")
                            positive_count += 1

                    elif resultult['compound'] < -0.2:
                        with open(r"out/negative_list_" + "%r" % string + r".txt", "a", encoding="utf-8") as outfile_comments:
                            outfile_comments.write(row[0] + "\n")
                            negative_count += 1

            print("\nDone.")

            plot_word_types(total_count, negative_count,
                            positive_count, string)


def main():
    '''Main method for the module.'''
    if len(sys.argv) == 1:
        run_sentiment_analysis()
    elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(
            "Usage: \n\tworkon reddit\n\tpython analysis.py [search term]|[option] [search term]")
    elif sys.argv[1] == "-w" or sys.argv[1] == "--words":
        search_string = str(sys.argv[2])
        search_type = str(sys.argv[3])
        filename = r"out/" + search_type.lower() + r"_list_" + \
            "%r" % search_string + r".txt"
        word_distribution(filename)
    else:
        search_string = str(sys.argv[1])
        run_topical_analysis(search_string)


if __name__ == '__main__':
    main()
