# TWITTER API DATA PROCESSING
---

## RUN
Python Version: 3.6.1

Run `pip install tweepy` on cmd
Fetch Twitter API Keys from here and feed into the `keys.py` key slots respectively. Keys can be fetched [here](//www.developers.twitter.com)
The format for running the program from command line is:
`python app.py keyword buffer`
Here, the first argument `keyword` will be the user desired keyword they want to track using Streaming API. The second argument `buffer` can be either 'one' or 'two' as string literals. 'one' corresponds to the first task of 1 minute tracking, and 'five' corresponds to the second task of 5 minutes tracking. Any other values passed to the uffer will default in 'one' (1).

## OUTPUT
The output prints out a report every minute on the conditions specified by the user and the question. The reports generated are:
- Username Reports
- Link Reports
- Unique Words Reports

## FEATURES
- One script, two choices for execution
- Uses thread
- Discards `t.co/xyz` when counting unique words
- Treats words equal, regardless of uppercase/lowercase for proper data collection
 
 ## SCOPE
 - More stop words can be added
 - The generated report can be saved in a pdf
 - More flexibility + help options when writing command line arguments
 - Filter out the retweets if required
