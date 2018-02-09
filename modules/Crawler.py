#-*- coding:utf-8 -*-

import hashlib
from collections import deque
import './BloomFilter'


class Crawler:

    downloaded_urls = []
    dum_md5_file = "./download.txt"
    time_out_file = "./data/time_out.log"
    bloom_download_urls = BloomFilter(1024 * 1024 * 16, 0.01)
    cur_queue = deque()


    def __init__(self):
        try:
            self.dum_file = open(dum_md5_file, 'r')
            self.downloaded_urls = self.dum_file.readlines()
            self.dum_file.close()
            for md5url in self.downloaded_urls:
                bloom_download_urls.add(md5url[:-1])
        except IOError:
            print('file not found')

        finally:
            self.dum_file = open(dum_md5_file, 'a')


    def enqueueUrl(self, url):
        if hashlib.md5(url.encode("utf-8")).hexdigest() not in self.bloom_download_urls:
            cur_queue.append(url)


    def dequeuUrl(self):
        try:
            url = cur_queue.popleft()
            return url
        except:
            return None


    def close(self):
        crawler.dum_file.close()

