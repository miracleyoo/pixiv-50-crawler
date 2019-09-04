# Author: Zhongyang Zhang
# E-mail: mirakuruyoo@gmail.com

import urllib
from urllib import request
from bs4 import BeautifulSoup
from datetime import date
import os
import requests
import argparse
import re
import time
import math
import codecs
import threading
import urllib.parse as up

class imgThread (threading.Thread):
    def __init__(self, threadID, pairs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = "Thread-"+str(threadID)
        self.counter = threadID
        self.pairs = pairs

    def run(self):
        log("Starting " + self.name)
        for pair in self.pairs:
            get_img(*pair)
        log("Exiting " + self.name)

def log(*args, end=None):
    if end is None:
        print(time.strftime("==> [%Y-%m-%d %H:%M:%S]",
                            time.localtime()) + " " + "".join([str(s) for s in args]))
    else:
        print(time.strftime("==> [%Y-%m-%d %H:%M:%S]", time.localtime()) + " " + "".join([str(s) for s in args]),
              end=end)

def recursion_worker(in_url, in_path):
    if len(in_url.split('/')[-1].split('.'))>1:
        if in_url.split('/')[-1].split('.')[-1] != 'zip':
            all_img_links.append([in_url, in_path])
        # get_img(in_url, in_path)
    else:
        folder_name = in_url.rstrip('/').split('/')[-1]
        if not os.path.exists(os.path.join(in_path, folder_name)):os.mkdir(os.path.join(in_path, folder_name))
        html = str(request.urlopen(in_url).read(), 'utf-8')
        soup = BeautifulSoup(html, 'lxml')
        out_urls = ['https://pic.tjsky.net'+i.attrs['href'] for i in soup.body.select('.mdui-container .mdui-container-fluid')[1].select('.nexmoe-item .mdui-row .mdui-list li a[href]')][1:]
        if out_urls[-1].split('/')[-2].startswith('.page'):
            html = str(request.urlopen(in_url+'.page-2/').read(), 'utf-8')
            soup = BeautifulSoup(html, 'lxml')
            out_urls = out_urls[:-1]
            urls_page2 = ['https://pic.tjsky.net'+i.attrs['href'] for i in soup.body.select('.mdui-container .mdui-container-fluid')[1].select('.nexmoe-item .mdui-row .mdui-list li a[href]')][1:-1]
            out_urls.extend(urls_page2)
        for out_url in out_urls:
            recursion_worker(out_url, os.path.join(in_path, folder_name))

def get_img(url, outpath):
    img_name = re.sub('-+', '-', '-'.join(up.unquote(url).split('/')[-1].split(' ')))
    img_path = os.path.join(outpath, img_name)
    try:
        img = requests.get(url)
        with open(img_path, 'wb') as f:
            f.write(img.content)
            f.flush()
        log("Successfully crawled img:{}".format(img_name[:60]))
    except:
        log("Failed crawling img:{}".format(url))

def main(url, outpath):
    rec_paths = url.rstrip('/').split('/')[3:-1]
    for r_path in rec_paths:
        if not os.path.exists(os.path.join(outpath, r_path)):
            os.mkdir(os.path.join(outpath, r_path))
        outpath=os.path.join(outpath, r_path)

    recursion_worker(url, outpath)

    log('Start crawling image links...')

    def chunks(arr, m):
        n = int(math.floor(len(arr) / float(m)))
        return [*[arr[i:i + n] for i in range(0, (m-1)*n, n)],arr[(m-1)*n:]]

    threads = []
    links_sep = chunks(all_img_links, opt.thread_num)

    for i in range(opt.thread_num):
        threads.append(imgThread(i, links_sep[i]))

    for i in threads:
        i.start()

    for i in threads:
        i.join()
    log('Successfully crawled all of the images. Thanks for using.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--initial_url', default='https://pic.tjsky.net/pixiv/pic/2019/', help='The initial url you want to crawl.')
    parser.add_argument('--tp', help='The time period you want to crawl, with a format like yyyy/mm/dd, or yyyy/mm or yyyy.')
    parser.add_argument('--initial_path', default='', help='The initial url you want to crawl.')
    parser.add_argument('--thread_num', type=int, default=3, help='The number of threads you want to use when crawling.')
    parser.add_argument('--today', '-t', action='store_true', help='Crawl the best images today')
    opt = parser.parse_args()
    if opt.tp is not None:
        if len(opt.tp.split('/'))==3:
            opt.initial_url = 'https://pic.tjsky.net/pixiv/pic/' + opt.tp.strip('/') + '_daily/'
        else:
            opt.initial_url = 'https://pic.tjsky.net/pixiv/pic/' + opt.tp.strip('/') + '/'
    if opt.today:
        today = date.today()
        opt.initial_url = 'https://pic.tjsky.net/pixiv/pic/'+str(today.year)+'/'+(str(today.month) if today.month>9 else '0'+str(today.month))+'/'+(str(today.day) if today.day>9 else '0'+str(today.day))+'_daily/'
    print(opt.initial_url)
    all_img_links = []
    main(opt.initial_url, opt.initial_path)
