from wxpy import *
import json
import requests


bot = Bot()
# bot = Bot(cache_path=True)

my_friend = bot.friends().search('GC_in_HK')[0]

friends_stat = bot.friends().stat()

friend_loc = []
for province, count in friends_stat['province'].iteritems():
    if province != '':
        friend_loc.append([province, count])

friend_loc.sort(key=lambda x: x[1], reverse=True)

for item in friend_loc[:10]:
    print(item[0], item[1])

