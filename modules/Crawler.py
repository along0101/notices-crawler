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
        self.dum_file.close()



'''
进一步工作
'''
MAX_THREAD = 20
CRAWL_DELAY = 0.5
#threads = []

model = {}

while True:  
    url = crawler.dequeue()  
    if url is None:  
       for t in threads:  
           t.join()  
           break  
    else:  
         while True:  
           for t in threads:  
               if not t.is_alive():  
                  threads.remove(t)  
           if len(threads) >= maxthreads  
               time.sleep(CRAWL_DELAY)  
               continue  
    try:  
         t =threading.Thread(target = get_page_content,name=None,args =url,stock,model)  
         threads.append(t)  
         t.setDaemon(True)  
         t.start()  
         time.sleep(CRAWL_DELAY)  
         break  
    except:  
         print("进入不了线程") 

#http://blog.csdn.net/a980135330/article/details/78161388

def get_page_content(url,stock,model):  
        stock_page = etree.HTML(get_text(url[1]))  
        notice = stock_page.xpath('//div[@class="detail-body"]/div[1]')[0].text  
  
        path = '/home/gupiao/%s/%s'%(stock,url[0][:4])  
        isExist = os.path.exists(path)  
          
        if not isExist:  
           os.makedirs(path)  
           print(path+"创建成功")  
          
        if url[0] in model.keys():  
           new_value = model[url[0]] + notice  
           model[url[0]] = new_value  
        else:  
           model[url[0]] = notice  
          
        mdurl = url[1].encode('utf8')  
        new_md5 = hashlib.md5(mdurl).hexdigest()  
        crawler.dumd5_file.write(new_md5+"\n") 


for talk_time in model.keys():  
    with open('/home/gupiao/%s/%s/%s.json'%(stock,talk_time[:4],talk_time[:7]),'a',encoding='utf-8') as json_file:  
              infodict = {}  
              infodice[talk_time] = model[talk_time]  
              json.dump(infodict,json_file,ensure = Flase)  
   print(stock+"完成") 