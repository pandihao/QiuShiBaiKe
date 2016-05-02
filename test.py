#!/user/bin/env python3
# _*_ coding: utf-8 _*_

from qshi import HotQiushi, User

url = "http://www.qiushibaike.com"
user_url = 'http://www.qiushibaike.com/users/24409811/'

qiushi = HotQiushi(url)
user = User(user_url)

items = qiushi.get_hot_contents()
for (vote, item) in items:
    print('Vote: {0} Content: {1}'.format(vote, item))


auth = qiushi.get_auth()
stats = qiushi.get_stats()
content = qiushi.get_content()
print('author: {0}\t stats: {1}\ncontent: {2} '.format(auth, stats, content))
print('_*_'*20)
save_txt = qiushi.to_txt()

info = user.user_info()
print('User information: ', info)
print('_*_ '*20)
url_list = user.get_atricle_url()
print('URL list: ', url_list)
print('_*_'*20)
scandals = user.scandal()
for item in scandals:
    print('Scandal: ', item)


print('_*_'*20)
top_scandal = user.get_top_i_scandal(3)
for vote, con in top_scandal:
    print('Stat: {0}\t Content: {1}'.format(vote, con))