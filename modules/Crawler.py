#-*- coding:utf-8 -*-

import hashlib
from collections import deque
import './PyBloom'


class Crawler(object):
    """
    爬虫，用于爬取东方财富中的股票公告内容
    """
    driver = None
    downloaded_urls = []
    dum_md5_file = "./download.txt"
    time_out_file = "./data/time_out.log"
    #bloom_download_urls = BloomFilter(1024 * 1024 * 16, 0.01)
    cur_queue = deque()

    def __init__(self):
        super(Crawler, self).__init__()

        '''读取下载(爬取)记录'''
        try:
            self.dum_file = open(self.dum_md5_file, 'r')
            self.downloaded_urls = self.dum_file.readlines()
            self.dum_file.close()
            '''
            for md5url in self.downloaded_urls:
                self.bloom_download_urls.add(md5url[:-1])
            '''
        except IOError:
            self.dum_file = open(self.dum_md5_file, 'a', encoding='utf-8')
            self.dum_file.close()

        '''初始化浏览器'''
        cap = dict(DesiredCapabilities.CHROME)
        cap["version"] = "63.0.3239.84"
        cap["javascriptEnabled"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=cap, service_args=['--load-images=no'])
        self.driver.set_page_load_timeout(10) #页面超时时间
        self.driver.set_window_size(1980, 1140)
        self.driver.implicitly_wait(10) #寻找一个元素的时间
        

    '''请求获取股票列表的数据'''
    def get_stock_list(self):
        db = pymysql.connect(host="192.168.0.103", user="root",
                     password="123456", db="chocolate", charset='utf8mb4', port=3007)

        sql = "select `real`,`code`,`name`,`status` from company where 1"

        with db.cursor() as cursor:
            cursor.execute(sql)
            stocks = cursor.fetchall()
        db.close()
        self.stocks = stocks
        return self.stocks


    '''获取网页源代码内容'''
    def get_text(self,url,max_retries = 1):
        i = 0
        while i < max_retries:
            try:
                self.driver.get(url)
                html_page = self.driver.page_source
                return html_page
            except Exception as e:
                i += 1
                print('time_out,retries %d.' % i, date, "ext", e)
                '''记日志'''
                if max_retries == i:
                    file = open(self.time_out_file, 'a', encoding='utf-8')
                    file.write('%s\n' % url)
                    file.close()

    '''请求链接，打开页面'''
    def request(self,item,stock,max_retries = 1):
        i = 0
        while i < max_retries:
            try:
                date,url = item
                ymd = date.split("-")
                md5_url = md5(url.encode('utf-8')).hexdigest()
                #去重处理
                if md5_url + "\n" in self.downloaded_urls:
                    print("pass", date, url)
                    break

                self.driver.get(url)
                title = self.driver.find_element_by_css_selector('div.content.clearfix>div.cont_txt>div.detail-header>h1').text
                title = title.split(" ")[0]
                content = self.driver.find_element_by_css_selector("div.content.clearfix>div.cont_txt>div.detail-body>div:nth-child(1)").text
                pdfLink = self.driver.find_element_by_css_selector('div.cont_txt>div.detail-body>div:nth-child(2)>a').get_attribute("href")
                
                fileName = md5_url + ".json"
                dir = './data/%s/%s/%s/' % (stock[0], ymd[0], "-".join(ymd[0:2]))
                if not os.path.exists(dir):
                    os.makedirs(dir)
                file = open(os.path.join(dir, fileName), 'w+', encoding='utf-8')
                file.write('{"org_code":"%s","org_name":"%s","origin_url":"%s","title":"%s","content":"%s"}' % (stock[0], stock[1], pdfLink, title, content))
                file.close()

                print("success", stock[0], date)
                self.downloaded_urls.append(md5_url)
                #self.bloom_download_urls.add(md5_url)
                self.dum_file = open(self.dum_md5_file, 'a', encoding='utf-8')
                self.dum_file.write(md5_url + "\n")
                self.dum_file.close()
                break
            except Exception as e:
                i += 1
                print('time_out,retries %d.' % i, date, "ext", e)
                '''记日志'''
                if max_retries == i:
                    file = open(self.time_out_file, 'a', encoding='utf-8')
                    file.write('%s\n' % url)
                    file.close()


    '''关闭浏览器'''
    def close(self):
        self.driver.quit()


class Crawler:

    downloaded_urls = []
    dum_md5_file = "./download.txt"
    time_out_file = "./data/time_out.log"
    bloom_download_urls = BloomFilter(1024 * 1024 * 128, 0.01)
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