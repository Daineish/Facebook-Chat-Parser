# Facebook-Chat-Parser
A facebook char parser which takes a json conversation file as input (downloaded from facebook) and parses the conversation to give some interesting stats about the conversation.

To download a conversation, go to facebook > settings > your facebook information > download a copy of your information. To use this parser, select messages, and change the format from HTML to JSON.

Current Features:

1. Total number of messages.
2. Most common messages.
3. Most common words.
4. Unique words.
5. Charts:
    a) Messages sent per hour of the day.
    b) Messages sent per day of the week.
    c) Messages sent per month of the year.
    d) Messages sent per year.
    e) Messages sent per month.

Restraints:

1. Only words for two people in a conversation.
2. Facebook seems to change their format for messages from time-to-time, works as of Sep. 2018.
3. Only tested with python 2.7.

Usage:

Ensure python 2.7 is downloaded on your machine. Use pip to download numpy, matplotlib, calendar, nltk (others?).

Download stopwords from nltk. See https://stackoverflow.com/questions/41348621/ssl-error-downloading-nltk-data. Only nltk.download('stopwords') is needed. Can also run python -m nltk.downloader stopwords.

Notes:

This was intended to be used as an introduction to Python for myself, along with as a fun project to share with a friend (whom I chat over FB messenger with frequently). This was not intended to be a showcase of good Python development or good programming practices, so view accordingly!
