import json
from pprint import pprint
from collections import Counter
import datetime

def decimal_to_percent(decimal):
    return "{0:.2f}".format(decimal*100) + '%'

def to_percent(top, bottom):
    return decimal_to_percent((float)( (float)(top) / (float)(bottom) ))

print 'Starting program...\n'

print 'Opening file ', './TestFiles/DaineMcNiven/message.json', '...'
with open('./TestFiles/DaineMcNiven/message.json') as f:
    print 'Loading data from file ...'
    data = json.load(f)
    list_of_messages = data['messages']

print 'Finished loading data...'

num_messages = len(list_of_messages)

first_message_time = datetime.datetime.fromtimestamp(int(list_of_messages[0]['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
last_message_time  = datetime.datetime.fromtimestamp(int(list_of_messages[num_messages-1]['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
total_time = int(list_of_messages[num_messages-1]['timestamp']) - int(list_of_messages[0]['timestamp'])
total_days = (total_time / 60 / 60 / 24)

print 'Parsing data...'

# Parse messages by sender
messages_from_daine = [x for x in list_of_messages if x['sender_name'] == u'Daine McNiven']
messages_from_tessa = [x for x in list_of_messages if x['sender_name'] == u'Tessa Heiydt']
#messages_from_other = [x for x in list_of_messages if x['sender_name'] != u'Daine McNiven' and x['sender_name'] != u'Tessa Heiydt'] #should be empty

num_messages_tessa = len(messages_from_tessa)
num_messages_daine = len(messages_from_daine)

# Parse content of messages by each sender
content_from_daine = [d['content'] for d in messages_from_daine if 'content' in d]
content_from_tessa = [d['content'] for d in messages_from_tessa if 'content' in d]

most_common_messages_daine = Counter(content_from_daine).most_common(10)
most_common_messages_tessa = Counter(content_from_tessa).most_common(10)

# Parse words from each message
words_from_daine = [word for l in content_from_daine for word in l.split()]
words_from_tessa = [word for l in content_from_tessa for word in l.split()]

num_words_daine = len(words_from_daine)
num_words_tessa = len(words_from_tessa)

most_common_words_daine = Counter(words_from_daine).most_common(10)
most_common_words_tessa = Counter(words_from_tessa).most_common(10)

num_unique_words_daine = len(set(words_from_daine))
num_unique_words_tessa = len(set(words_from_tessa))

love_count_daine = (words_from_daine).count('love') + (words_from_daine).count('Love')
love_count_tessa = (words_from_tessa).count('love') + (words_from_tessa).count('Love')



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
print 'Times "Love" said: ', love_count_tessa, '(', to_percent(love_count_tessa, num_words_tessa), ')\n'


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
print 'Times "Love" said: ', love_count_daine, '(', to_percent(love_count_daine, num_words_daine), ')\n'

