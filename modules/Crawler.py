#-*- coding:utf-8 -*-

import hashlib
# from pybloomfilter import BloomFilter


class Crawler:

    downloaded_urls = []
    dum_md5_file = '文件路径'
    bloom_download_urls = BloomFilter(1024 * 1024 * 16, 0.01)
    cur_queue = deque()

    def __init__(self):
        try:
            self.dum_file = open(dum_md5_file, 'r')
            self.downloaded_urls = self.dun_file.readlines()
            self.dum_file.close()
            for urlmd5 in self.downloaded_urls:
                bloom_download_urls.add(urlmd5[:-1])
        except IOError:
            print('file not found')

        finally:
            self.dum_file = open(dum_md5_file, 'a')


    def enqueueUrl(self, url):
        if hashlib.md5(url).hexdigest() not in self.bloom_download_urls:
            cur_queue.append(url)


    def dequeuUrl(self):
        try:
            url = cur_queue.popleft()
            return url
        except:
            return None


    def close(self):
        crawler.dum_file.close()
