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
def make_barchart(numX, yValsA, yValsB, title='', ylabel='Number of Messages', xticks=None, xticksorient='vertical', yValsAName='Tessa', yValsBName='Daine', colorA='purple', colorB='aqua', barwidth=0.4):
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
print 'Opening file ', './TestFiles/DaineMcNiven/message.json', '...'
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
messages_from_daine = [x for x in list_of_messages if x['sender_name'] == u'Daine McNiven']
messages_from_tessa = [x for x in list_of_messages if x['sender_name'] == u'Tessa Heiydt']
#messages_from_other = [x for x in list_of_messages if x['sender_name'] != u'Daine McNiven' and x['sender_name'] != u'Tessa Heiydt'] #should be empty

num_messages_tessa = len(messages_from_tessa)
num_messages_daine = len(messages_from_daine)

# Parse content of messages by each sender
content_from_daine = [d['content'].lower() for d in messages_from_daine if 'content' in d]
content_from_tessa = [d['content'].lower() for d in messages_from_tessa if 'content' in d]

most_common_messages_daine = Counter(content_from_daine).most_common(10)
most_common_messages_tessa = Counter(content_from_tessa).most_common(10)

# Parse words from each message
words_from_daine = [word for l in content_from_daine for word in l.split()]
words_from_daine_no_stopwords = [x for x in words_from_daine if x not in g_stopwords]
words_from_tessa = [word for l in content_from_tessa for word in l.split()]
words_from_tessa_no_stopwords = [x for x in words_from_tessa if x not in g_stopwords]

num_words_daine = len(words_from_daine)
num_words_tessa = len(words_from_tessa)

most_common_words_daine = Counter(words_from_daine_no_stopwords).most_common(10)
most_common_words_tessa = Counter(words_from_tessa_no_stopwords).most_common(10)

num_unique_words_daine = len(set(words_from_daine))
num_unique_words_tessa = len(set(words_from_tessa))

if len(sys.argv) != 3:
    # Find messages by hours
    messages_by_hour_daine = [0] * 24
    messages_by_hour_tessa = [0] * 24
    for i in range(0, 24):
        messages_by_hour_daine[i] = len([x for x in messages_from_daine if datetime.datetime.fromtimestamp(int(x['timestamp'])).hour == i])
        messages_by_hour_tessa[i] = len([x for x in messages_from_tessa if datetime.datetime.fromtimestamp(int(x['timestamp'])).hour == i])

    xticks = tuple([datetime.time(i).strftime('%I %p') for i in range(24)])
    make_barchart(24, messages_by_hour_tessa, messages_by_hour_daine, 'Number of Messages by Hour', xticks=xticks)

    # Find messages by Day of Week
    messages_by_dayofweek_daine = [0] * 7
    messages_by_dayofweek_tessa = [0] * 7
    for i in range(0, 7):
        messages_by_dayofweek_daine[i] = len([x for x in messages_from_daine if datetime.datetime.fromtimestamp(int(x['timestamp'])).weekday() == i])
        messages_by_dayofweek_tessa[i] = len([x for x in messages_from_tessa if datetime.datetime.fromtimestamp(int(x['timestamp'])).weekday() == i])

    make_barchart(7, messages_by_dayofweek_tessa, messages_by_dayofweek_daine, 'Number of Messages by Day of Week', xticks=calendar.day_abbr)

    # Find messages by Month
    messages_by_month_daine = [0] * 12
    messages_by_month_tessa = [0] * 12
    for i in range(1, 13):
        messages_by_month_daine[i-1] = len([x for x in messages_from_daine if datetime.datetime.fromtimestamp(int(x['timestamp'])).month == i])
        messages_by_month_tessa[i-1] = len([x for x in messages_from_tessa if datetime.datetime.fromtimestamp(int(x['timestamp'])).month == i])

    make_barchart(12, messages_by_month_tessa, messages_by_month_daine, 'Number of Messages by Month', xticks=calendar.month_abbr[1:13])

    # Find messages by Year
    messages_by_year_daine = [0] * numYears
    messages_by_year_tessa = [0] * numYears
    for i in range(yearBegin, yearEnd+1):
        messages_by_year_daine[i-yearBegin] = len([x for x in messages_from_daine if datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i])
        messages_by_year_tessa[i-yearBegin] = len([x for x in messages_from_tessa if datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i])

    make_barchart(numYears, messages_by_year_tessa, messages_by_year_daine, 'Number of Messages by Year', xticks=tuple(range(yearBegin, yearEnd+1)))

    # Find messages by Year & Month
    messages_by_yearmonth_daine = [0] * (12 * numYears)
    messages_by_yearmonth_tessa = [0] * (12 * numYears)
    for i in range(yearBegin, yearEnd+1):
        for j in range(1, 13):
            messages_by_yearmonth_daine[(i-yearBegin)*12+(j-1)] = len([x for x in messages_from_daine if (datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i and datetime.datetime.fromtimestamp(int(x['timestamp'])).month == j)])
            messages_by_yearmonth_tessa[(i-yearBegin)*12+(j-1)] = len([x for x in messages_from_tessa if (datetime.datetime.fromtimestamp(int(x['timestamp'])).year == i and datetime.datetime.fromtimestamp(int(x['timestamp'])).month == j)])

    xticks = []

    for year in range(yearBegin, yearEnd+1):
        xticks.append(str(year))
        for i in range(0, 11):
            xticks.append('')
    make_barchart(12*(numYears), messages_by_yearmonth_tessa, messages_by_yearmonth_daine, 'Number of Messages by Year and Month', xticks=xticks)

#plt.show()
    plt.draw()

# Print data
print '\nSummary\n======='
print 'Total messages: ', num_messages, ' from ', first_message_time, ' to ', last_message_time
print 'That\'s ', total_days, ' days and ', num_messages/total_days, ' messages per day!\n'

# Tessa
print 'Tessa:\n-----\n', num_messages_tessa, ' messages (', to_percent(num_messages_tessa, num_messages), ')'

# Messages
print 'Most Common Messages'
max_val = min(10, len(most_common_messages_tessa)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_messages_tessa[i][0], '" said ', most_common_messages_tessa[i][1], ' times (', to_percent(int(most_common_messages_tessa[i][1]), num_messages_tessa), '),'
print '\t', max_val+1, ': ', most_common_messages_tessa[max_val][0], '" said ',most_common_messages_tessa[max_val][1], ' times (', to_percent(int(most_common_messages_tessa[max_val][1]), num_messages_tessa), ').'

#Words
print 'Most Common Words'
max_val = min(10, len(most_common_words_tessa)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_words_tessa[i][0], '" said ', most_common_words_tessa[i][1], ' times (', to_percent(int(most_common_words_tessa[i][1]), num_words_tessa), '),'
print '\t', max_val+1, ': "', most_common_words_tessa[max_val][0], '" said ',most_common_words_tessa[max_val][1], ' times (', to_percent(int(most_common_words_tessa[max_val][1]), num_words_tessa), ').'

print 'Unique Words Said: ', num_unique_words_tessa, ' giving a diversity index of: ', to_percent(num_unique_words_tessa, num_words_tessa)


# Daine
print 'Daine:\n-----\n', num_messages_daine, ' messages (', to_percent(num_messages_daine, num_messages), ')'

# Messages
print 'Most Common Messages'
max_val = min(10, len(most_common_messages_daine)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_messages_daine[i][0], '" said ', most_common_messages_daine[i][1], ' times (', to_percent(int(most_common_messages_daine[i][1]), num_messages_daine), '),'
print '\t', max_val+1, ': "', most_common_messages_daine[max_val][0], '" said ',most_common_messages_daine[max_val][1], ' times (', to_percent(int(most_common_messages_daine[max_val][1]), num_messages_daine), ').'

# Words
print 'Most Common Words'
max_val = min(10, len(most_common_words_daine)-1)
for i in range(0, max_val):
    print '\t', i+1, ': "', most_common_words_daine[i][0], '" said ', most_common_words_daine[i][1], ' times (', to_percent(int(most_common_words_daine[i][1]), num_words_daine), '),'
print '\t', max_val+1, ': "', most_common_words_daine[max_val][0], '" said ',most_common_words_daine[max_val][1], ' times (', to_percent(int(most_common_words_daine[max_val][1]), num_words_daine), ').'

print 'Unique Words Said: ', num_unique_words_daine, ' giving a diversity index of: ', to_percent(num_unique_words_daine, num_words_daine)

if len(sys.argv) != 3:
    plt.show()
