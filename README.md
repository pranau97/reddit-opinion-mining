# Reddit Opinion Mining and Sentiment Analysis

A project written in R and Python to mine a Reddit corpus.

## Requirements

### Python and its dependencies

1. Python 3
2. PRAW
3. requests
4. bs4
5. numpy
6. fuzzywuzzy
7. nltk
8. matplotlib

**Recommended:** Install python related packages in a virtual environment.

Install using `pip install -U <package-name>`. NLTK also requires that you install the corpuses for tokens and stopwords for the English language.

### R and its dependencies

1. R
2. sna
3. ggnetwork
4. svglite
5. igraph
6. intergraph
7. rsvg
8. ggplot2

Install using `install.packages(<package-name>)`.

## Obtaining Reddit API access credentials

1. Create a Reddit account, and while logged in, navigate to preferences > apps
2. Click on the `Are you a developer? Create an app...` button
3. Fill in the details-
    * name: Name of your bot/script
    * Select the option 'script'
    * description: Put in a description of your bot/script
    * redirect uri: `http://localhost:8080`
4. Click on `Create App`.
5. You will be given a `client_id` and a `client_secret`. Keep them confidential.

## Extracting edge data from the Pushshift Reddit dataset

1. Sign up / login on [Google BigQuery](https://bigquery.cloud.google.com).
2. Select or create a new project and click on 'Compose Query'.
3. Paste the contents of the SQL script in the folder `subreddit-viz` in the editor and run it.
4. Download the generated CSV file as `reddit-edge-list.csv` and save it within the `subreddit-viz` folder.

## Running the scripts

1. To obtain the subreddit visualizations, run the R script using `R CMD BATCH reddit.R`. Make sure to create an empty folder called `subreddit-groups` in the same folder as the script.
2. Create a file named `praw.ini` with it's contents as:
    ```plaintext
    [<bot-name>]
    username: reddit username
    password: reddit password
    client_id: client_id that you got
    client_secret: client_secret that you got
    ```
3. Run the script `getdata.py` via `python3 getdata.py`.
4. It should scrape all the necessary data in approximately 20-25 minutes.
5. Run `analysis.py` using `python3 analysis.py [args]`. The arguments the script accepts are -
    * no arguments - Runs sentiment analysis on the entire data.
    * `-h` or `--help` - Prints the usage details.
    * `-w string type` or `--words string type` - Generates a word distribution of the given string and type - positive or negative. Requires that sentiment analysis for the particular term already be performed previously.
    * `string` - Looks for similar strings in the corpus and performs sentiment analysis on it.

## Credits

* Max Woolf's blog post on [subreddit visualizations](http://minimaxir.com/2016/05/reddit-graph/) was of great help in making this project.