import sys
import string
import json
from pprint import pprint
from collections import Counter
import datetime
import calendar
import numpy
import matplotlib.pyplot as plt
import nltk

####### Definitions #######
def decimal_to_percent(decimal):
    return "{0:.2f}".format(decimal*100) + '%'

def to_percent(top, bottom):
    return decimal_to_percent((float)( (float)(top) / (float)(bottom) ))

"""
    Creates a barchart with two sets of data.
    
    Args:
        numX: The number of different x values.
        yValsA: A list of the first set of y values. len(yValsA) should == numX
        yValsB: A list of the second set of y values. len(yValsB) should == numX
        title: The title of the barchart.
        ylabel: The label on the y axis.
        xticks: A tuple of the values to go along the x-axis. The tuple should have numX values.
        xticksorient: The rotation of the values on the x axis, can be specified in degrees or keywords.
        yValsAName: The name of the yValsA data to go in the legend.
        yValsBName: The name of the yValsB data to go in the legend.
        colorA: The color of the yValsA data.
        colorB: The color of the yValsB data.
        barwidth: The width of the bars.
"""
def make_barchart(numX, yValsA, yValsB, title='', ylabel='Number of Messages', xticks=None, xticksorient='vertical', yValsAName='P2', yValsBName='P1', colorA='purple', colorB='aqua', barwidth=0.4):
    make_barchart.num_charts += 1
    plt.figure(make_barchart.num_charts)
    plt.subplot(111)
    p1 = plt.bar(numpy.arange(numX)-(barwidth/2.0), yValsA, barwidth, color=colorA)
    p2 = plt.bar(numpy.arange(numX)+(barwidth/2.0), yValsB, barwidth, color=colorB)
    plt.ylabel(ylabel)
    plt.title(title)
    if xticks:
        plt.xticks(numpy.arange(numX), xticks, rotation=xticksorient)
    plt.legend((p1[0], p2[0]), (yValsAName, yValsBName))
make_barchart.num_charts = 0

g_stopwords = set( nltk.corpus.stopwords.words('english'))
####### End Definitions #######

if len(sys.argv) > 3 or len(sys.argv) == 1 or (len(sys.argv) == 3 and sys.argv[2] != 'nocharts'):
    print 'Usage: "python fbparser.py filename.json" to create data and charts, or\n"python fbparser.py filename.json nocharts" to disable creating charts'
    exit()

print 'Starting program...\n'
print 'Opening file ', sys.argv[1], '...'
with open(sys.argv[1]) as f:
    print 'Loading data from file ...'
    data = json.load(f)
    list_of_messages = data['messages']

print 'Finished loading data...'

num_messages = len(list_of_messages)
smallest_time = int(list_of_messages[0]['timestamp'])
largest_time  = int(list_of_messages[0]['timestamp'])
for msg in list_of_messages:
    if int(msg['timestamp']) < smallest_time:
        smallest_time = int(msg['timestamp'])
    if int(msg['timestamp']) > largest_time:
        largest_time = int(msg['timestamp'])
yearBegin = datetime.datetime.fromtimestamp(smallest_time).year
yearEnd   = datetime.datetime.fromtimestamp(largest_time).year
numYears = (yearEnd - yearBegin) + 1
first_message_time = datetime.datetime.fromtimestamp(smallest_time).strftime('%Y-%m-%d %H:%M:%S')
last_message_time  = datetime.datetime.fromtimestamp(largest_time ).strftime('%Y-%m-%d %H:%M:%S')
total_time = largest_time - smallest_time
total_days = (total_time / 60 / 60 / 24)

print 'Parsing data...'

# Parse messages by sender
people_in_conversation = []
for x in list_of_messages:
    if x['sender_name'] not in people_in_conversation:
        people_in_conversation.append(x['sender_name'])
if len(people_in_conversation) < 2:
    print 'Must have at least two people in the conversation.'
    exit()
if len(people_in_conversation) > 2:
    print 'This program is meant for only 2 person conversations, using ', people_in_conversation[0], ' and ', people_in_conversation[1], '.'

messages_from_p1 = [x for x in list_of_messages if x['sender_name'] == people_in_conversation[0]]
messages_from_p2 = [x for x in list_of_messages if x['sender_name'] == people_in_conversation[1]]

num_messages_p1 = len(messages_from_p1)
num_messages_p2 = len(messages_from_p2)

# Parse content of messages by each sender
content_from_p1 = [d['content'].lower() for d in messages_from_p1 if 'content' in d]
content_from_p2 = [d['content'].lower() for d in messages_from_p2 if 'content' in d]

most_common_messages_p1 = Counter(content_from_p1).most_common(10)
most_common_messages_p2 = Counter(content_from_p2).most_common(10)

# Parse words from each message
words_from_p1 = [word for l in content_from_p1 for word in l.split()]
words_from_p1_no_stopwords = [x for x in words_from_p1 if x not in g_stopwords]
words_from_p2 = [word for l in content_from_p2 for word in l.split()]
words_from_p2_no_stopwords = [x for x in words_from_p2 if x not in g_stopwords]

num_words_p1 = len(words_from_p1)
num_words_p2 = len(words_from_p2)

most_common_words_p1 = Counter(words_from_p1_no_stopwords).most_common(10)
most_common_words_p2 = Counter(words_from_p2_no_stopwords).most_common(10)

num_unique_words_p1 = len(set(words_from_p1))
num_unique_words_p2 = len(set(words_from_p2))

if len(sys.argv) != 3:
    # Find messages by hours
    messages_by_hour_p1 = [0] * 24
    messages_by_hour_p2 = [0] * 24
    for i in range(0, 24):
        messages_by_hour_p1[i] = len([x for x in messages_from_p1 if datetime.datetime.fromtimestamp(int(x['timestamp'])).hour == i])
        messages_by_hour_p2[i] = len([x for x in messages_from_p2 if datetime.datetime.fromtimestamp(int(x['timestamp'])).hour == i])

    xticks = tuple([datetime.time(i).strftime('%I %p') for i in range(24)])
    make_barchart(24, messages_by_hour_p2, messages_by_hour_p1, 'Number of Messages by Hour', xticks=xticks, yValsAName = people_in_conversation[1], yValsBName = people_in_conversation[0])

    # Find messages by Day of Week
    messages_by_dayofweek_p1 = [0] * 7
    messages_by_dayofweek_p2 = [0] * 7
    for i in range(0, 7):
        messages_by_dayofweek_p1[i] = len([x for x in messages_from_p1 if datetime.datetime.fromtimestamp(int(x['timestamp'])).weekday() == i])
        messages_by_dayofweek_p2[i] = len([x for x in messages_from_p2 if datetime.datetime.fromtimestamp(int(x['timestamp'])).weekday() == i])

    make_barchart(7, messages_by_dayofweek_p2, messages_by_dayofweek_p1, 'Number of Messages by Day of Week', xticks=calendar.day_abbr, yValsAName = people_in_conversation[1], yValsBName = people_in_conversation[0])

    # Find messages by Month
    messages_by_month_p1 = [0] * 12
    messages_by_month_p2 = [0] * 12
    for i in range(1, 13):
        messages_by_month_p1[i-1] = len([x for x in messages_from_p1 if datetime.datetime.fromtimestamp(int(x['timestamp'])).month == i])
        messages_by_month_p2[i-1] = len([x for x in messages_from_p2 if datetime.datetime.fromtimestamp(int(x['timestamp'])).month == i])

    make_barchart(12, messages_by_month_p2, messages_by_month_p1, 'Number of Messages by Month', xticks=calendar.month_abbr[1:13], yValsAName = people_in_conversation[1], yValsBName = people_in_conversation[0])

    # Find messages by Year
    messages_by_year_p1 = [0] * numYears
    messages_by_year_p2 = [0] * numYears
    for i in range(yearBegin, yearEnd+1):
        messages_by_year_p1[i-yearBegin] = len([x for x in messages_from_p1 if datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i])
        messages_by_year_p2[i-yearBegin] = len([x for x in messages_from_p2 if datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i])

    make_barchart(numYears, messages_by_year_p2, messages_by_year_p1, 'Number of Messages by Year', xticks=tuple(range(yearBegin, yearEnd+1)), yValsAName = people_in_conversation[1], yValsBName = people_in_conversation[0])

    # Find messages by Year & Month
    messages_by_yearmonth_p1 = [0] * (12 * numYears)
    messages_by_yearmonth_p2 = [0] * (12 * numYears)
    for i in range(yearBegin, yearEnd+1):
        for j in range(1, 13):
            messages_by_yearmonth_p1[(i-yearBegin)*12+(j-1)] = len([x for x in messages_from_p1 if (datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i and datetime.datetime.fromtimestamp(int(x['timestamp'])).month == j)])
            messages_by_yearmonth_p2[(i-yearBegin)*12+(j-1)] = len([x for x in messages_from_p2 if (datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i and datetime.datetime.fromtimestamp(int(x['timestamp'])).month == j)])

    xticks = []

    for year in range(yearBegin, yearEnd+1):
        xticks.append(str(year))
        for i in range(0, 11):
            xticks.append('')
    make_barchart(12*(numYears), messages_by_yearmonth_p2, messages_by_yearmonth_p1, 'Number of Messages by Year and Month', xticks=xticks, yValsAName = people_in_conversation[1], yValsBName = people_in_conversation[0])

    plt.draw()

# Print data
print '\nSummary\n======='
print 'Total messages: ', num_messages, ' from ', first_message_time, ' to ', last_message_time
print 'That\'s ', total_days, ' days and ', num_messages/total_days, ' messages per day!\n'

# P2
print people_in_conversation[1], ':\n-----\n', num_messages_p2, ' messages (', to_percent(num_messages_p2, num_messages), ')'

# Messages
print 'Most Common Messages'
max_val = min(10, len(most_common_messages_p2)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_messages_p2[i][0], '" said ', most_common_messages_p2[i][1], ' times (', to_percent(int(most_common_messages_p2[i][1]), num_messages_p2), '),'
print '\t', max_val+1, ': ', most_common_messages_p2[max_val][0], '" said ',most_common_messages_p2[max_val][1], ' times (', to_percent(int(most_common_messages_p2[max_val][1]), num_messages_p2), ').'

#Words
print 'Most Common Words'
max_val = min(10, len(most_common_words_p2)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_words_p2[i][0], '" said ', most_common_words_p2[i][1], ' times (', to_percent(int(most_common_words_p2[i][1]), num_words_p2), '),'
print '\t', max_val+1, ': "', most_common_words_p2[max_val][0], '" said ',most_common_words_p2[max_val][1], ' times (', to_percent(int(most_common_words_p2[max_val][1]), num_words_p2), ').'

print 'Unique Words Said: ', num_unique_words_p2, ' giving a diversity index of: ', to_percent(num_unique_words_p2, num_words_p2)


# P1
print people_in_conversation[0], ':\n-----\n', num_messages_p1, ' messages (', to_percent(num_messages_p1, num_messages), ')'

# Messages
print 'Most Common Messages'
max_val = min(10, len(most_common_messages_p1)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_messages_p1[i][0], '" said ', most_common_messages_p1[i][1], ' times (', to_percent(int(most_common_messages_p1[i][1]), num_messages_p1), '),'
print '\t', max_val+1, ': "', most_common_messages_p1[max_val][0], '" said ',most_common_messages_p1[max_val][1], ' times (', to_percent(int(most_common_messages_p1[max_val][1]), num_messages_p1), ').'

# Words
print 'Most Common Words'
max_val = min(10, len(most_common_words_p1)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_words_p1[i][0], '" said ', most_common_words_p1[i][1], ' times (', to_percent(int(most_common_words_p1[i][1]), num_words_p1), '),'
print '\t', max_val+1, ': "', most_common_words_p1[max_val][0], '" said ',most_common_words_p1[max_val][1], ' times (', to_percent(int(most_common_words_p1[max_val][1]), num_words_p1), ').'

print 'Unique Words Said: ', num_unique_words_p1, ' giving a diversity index of: ', to_percent(num_unique_words_p1, num_words_p1)

if len(sys.argv) != 3:
    plt.show()
