#!/user/bin/env python3
# _*_ coding: utf-8 _*_


import os
import collections
import requests
from bs4 import BeautifulSoup


class HotQiushi:
    soup = None
    url = None
    def __init__(self, url):
        if url != None:
            self.url = url

    def get_html(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, 'lxml')

    def get_auth(self):
        if self.soup == None:
            self.get_html()
        soup = self.soup
        auth = soup.find('div', class_='author clearfix').h2.get_text()
        return auth

    def get_content(self):
        if self.soup == None:
            self.get_html()
        soup = self.soup
        content = soup.find('div', class_='content').get_text()
        return content

    def get_hot_contents(self):
        if self.soup == None:
            self.get_html()
        soup = self.soup
        s = soup.find_all('div', class_='article block untagged mb15')
        if s is not None:
            for j in range(len(s)):
                vote = s[j].find('span', class_='stats-vote').i.get_text()
                contents = s[j].find('div', class_='content').get_text()
                yield (vote, contents)

    def to_txt(self):
        if os.path.exists(os.path.join(os.getcwd(), "Qiushi.txt")):
            with open(os.path.join(os.getcwd(), "Qiushi.txt"), 'a') as f:
                f.write('\n\n')
        else:
            for vote, item in self.get_hot_contents():
                with open(os.path.join(os.getcwd(), "Qiushi.txt"), 'a') as f:
                    f.write(item)

    def get_stats(self):
        if self.soup == None:
            self.get_html()
        soup = self.soup
        vote = soup.find('span', class_='stats-vote').i.get_text()
        return vote


class User:
    soup = None
    url = None
    home_url = 'http://www.qiushibaike.com/'

    def __init__(self, url):
        if url != None:
            self.url = url

    def parser(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, 'lxml')

    def user_info(self):
        alist = []
        if self.soup == None:
            self.parser()
        soup = self.soup

        user_name = soup.find('div', class_='user-header-cover').h2.get_text()
        alist.append(user_name)
        s = soup.find('div', class_='user-col-left').find_all('li')
        for j in range(11):
            value = s[j].get_text()
            alist.append(value)
        return alist

    def get_atricle_url(self):
        article_url = []
        if self.soup == None:
            self.parser()
        soup = self.soup
        s = soup.find_all('div', class_='user-block user-feed')
        if s is not None:
            for j in range(len(s)):
                article_url.append(s[j].find('li', class_='user-article-text').a['href'])
        return article_url

    def scandal(self):
        if self.soup == None:
            self.parser()
        soup = self.soup
        s = soup.find_all('div', class_='user-block user-feed')
        if s is not None:
            for j in range(len(s)):
                contents = s[j].find('li', class_='user-article-text').a.get_text()
                yield contents

    def get_top_i_scandal(self, n):
        adict = {}
        url_list = self.get_atricle_url()
        for i in range(len(url_list)):
            article_url = self.home_url + url_list[i]

            article = HotQiushi(article_url)
            adict[article_url] = article.get_stats()
        # lambda d: d[0]以key排序，lambda d: d[1]以value排序
        adict = collections.OrderedDict(sorted(adict.iteritems(), key=lambda d: d[1]))

        print('+-^-'*20)
        print(adict)
        print('+-^-'*20)

        alist = []
        for key in adict:
            alist.append(key)
            if len(alist) == n:
                break

        for url in alist:
            article = HotQiushi(url)
            contents = article.get_content()
            vote = article.get_stats()
            yield (vote, contents)