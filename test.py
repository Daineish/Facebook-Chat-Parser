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
num_messages_float = (float)(num_messages)

first_message_time = datetime.datetime.fromtimestamp(int(list_of_messages[0]['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
last_message_time  = datetime.datetime.fromtimestamp(int(list_of_messages[num_messages-1]['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
total_time = int(list_of_messages[num_messages-1]['timestamp']) - int(list_of_messages[0]['timestamp'])
total_days = (total_time / 60 / 60 / 24)

print 'Parsing data...'

messages_from_daine = [x for x in list_of_messages if x['sender_name'] == u'Daine McNiven']
messages_from_tessa = [x for x in list_of_messages if x['sender_name'] == u'Tessa Heiydt']
messages_from_other = [x for x in list_of_messages if x['sender_name'] != u'Daine McNiven' and x['sender_name'] != u'Tessa Heiydt'] #should be empty

content_from_daine = [d['content'] for d in messages_from_daine if 'content' in d]
content_from_tessa = [d['content'] for d in messages_from_tessa if 'content' in d]

most_common_messages_daine = Counter(content_from_daine).most_common(3)
most_common_messages_tessa = Counter(content_from_tessa).most_common(3)

words_from_daine = [word for l in content_from_daine for word in l.split()]
words_from_tessa = [word for l in content_from_tessa for word in l.split()]

most_common_words_daine = Counter(words_from_daine).most_common(3)
most_common_words_tessa = Counter(words_from_tessa).most_common(3)

unique_words_daine = set(words_from_daine)
unique_words_tessa = set(words_from_tessa)

percent_messages_daine = (float)((float)(len(messages_from_daine)) / num_messages_float)
percent_messages_tessa = (float)((float)(len(messages_from_tessa)) / num_messages_float)

diversity_daine = (float)((float)(len(unique_words_daine)) / (float)(len(words_from_daine)))
diversity_tessa = (float)((float)(len(unique_words_tessa)) / (float)(len(words_from_tessa)))

love_count_daine = (words_from_daine).count('love') + (words_from_daine).count('Love')
love_count_tessa = (words_from_tessa).count('love') + (words_from_tessa).count('Love')

num_messages_tessa = len(messages_from_tessa)
num_messages_daine = len(messages_from_daine)

num_words_daine = len(words_from_daine)
num_words_tessa = len(words_from_tessa)

num_unique_words_daine = len(unique_words_daine)
num_unique_words_tessa = len(unique_words_tessa)


print '\nSummary\n======='
print 'Total messages: ', num_messages, ' from ', first_message_time, ' to ', last_message_time
print 'That\'s ', total_days, ' days and ', num_messages/total_days, ' messages per day!\n'

print 'Tessa:\n-----\n', num_messages_tessa, ' messages (', to_percent(num_messages_tessa, num_messages), ')'
print 'Most Common Messages'
print '\t"', most_common_messages_tessa[0][0], '" said ', most_common_messages_tessa[0][1], ' times (', to_percent(int(most_common_messages_tessa[0][1]), num_messages_tessa), '),'
print '\t"', most_common_messages_tessa[1][0], '" said ', most_common_messages_tessa[1][1], ' times (', to_percent(int(most_common_messages_tessa[1][1]), num_messages_tessa), '), and'
print '\t"', most_common_messages_tessa[2][0], '" said ', most_common_messages_tessa[2][1], ' times (', to_percent(int(most_common_messages_tessa[2][1]), num_messages_tessa), ')!'
print 'Most Common Words'
print '\t', most_common_words_tessa[0][0], ' said ', most_common_words_tessa[0][1], ' times (', to_percent(int(most_common_words_tessa[0][1]), num_words_tessa), '),'
print '\t', most_common_words_tessa[1][0], ' said ', most_common_words_tessa[1][1], ' times (', to_percent(int(most_common_words_tessa[1][1]), num_words_tessa), '), and'
print '\t', most_common_words_tessa[2][0], ' said ', most_common_words_tessa[2][1], ' times (', to_percent(int(most_common_words_tessa[2][1]), num_words_tessa), ')!'
print 'Unique Words Said: ', num_unique_words_tessa, ' giving a diversity index of: ', to_percent(num_unique_words_tessa, num_words_tessa)
print 'Times "Love" said: ', love_count_tessa, '(', to_percent(love_count_tessa, num_words_tessa), ')\n'

print 'Daine:\n-----\n', num_messages_daine, ' messages (', to_percent(num_messages_daine, num_messages), ')'
print 'Most Common Messages'
print '\t"', most_common_messages_daine[0][0], '" said ', most_common_messages_daine[0][1], ' times (', to_percent(int(most_common_messages_daine[0][1]), num_messages_daine), '),'
print '\t"', most_common_messages_daine[1][0], '" said ', most_common_messages_daine[1][1], ' times (', to_percent(int(most_common_messages_daine[1][1]), num_messages_daine), '), and'
print '\t"', most_common_messages_daine[2][0], '" said ', most_common_messages_daine[2][1], ' times (', to_percent(int(most_common_messages_daine[2][1]), num_messages_daine), ')!'
print 'Most Common Words'
print '\t', most_common_words_daine[0][0], ' said ', most_common_words_daine[0][1], ' times (', to_percent(int(most_common_words_daine[0][1]), num_words_daine), '),'
print '\t', most_common_words_daine[1][0], ' said ', most_common_words_daine[1][1], ' times (', to_percent(int(most_common_words_daine[1][1]), num_words_daine), '), and'
print '\t', most_common_words_daine[2][0], ' said ', most_common_words_daine[2][1], ' times (', to_percent(int(most_common_words_daine[2][1]), num_words_daine), ')!'
print 'Unique Words Said: ', num_unique_words_daine, ' giving a diversity index of: ', to_percent(num_unique_words_daine, num_words_daine)
print 'Times "Love" said: ', love_count_daine, '(', to_percent(love_count_daine, num_words_daine), ')\n'
