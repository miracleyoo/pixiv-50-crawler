# pixiv50 scraw multi thread

## 背景说明

在网站 https://pic.tjsky.net/pixiv/ 上，会有专人每日更新经过筛选的Pixiv每日最佳50张图，且经过了手动的去重复，所以实际每天会有约30张图更新。相信喜欢浏览P站的朋友一定不少，但是苦于P站的每日最佳会混入漫画以及会有重复以及不便于整理收集、不便于爬取之前日期的每日最佳等原因会难以入手，这里提供一个好用的多线程Pixiv每日精选50图爬虫。

## 使用方法

爬虫可以指定某一天来爬取，也可以直接爬取一个月、一年的量，并按照原文件目录进行整理，且采用增量更新的方式，保持每次爬取后的文件目录一致，便于后续管理。

你甚至可以选择使用--today参数来直接爬取今天的图片集或使用—tp参数来直接指定时间而非输入网址。

另外，你可以选择同时使用的线程数目，默认为3，线程数越多速度越快，但请注意，线程数过高时可能会出现空文件现象，不建议设置过高。

具体帮助如下：

```bash
usage: pixiv50_scraw_multi_thread.py [-h] [--initial_url INITIAL_URL]
                                     [--tp TP] [--initial_path INITIAL_PATH]
                                     [--thread_num THREAD_NUM] [--today]

optional arguments:
  -h, --help            show this help message and exit
  --initial_url INITIAL_URL
                        The initial url you want to crawl.
  --tp TP               The time period you want to crawl, with a format like
                        yyyy/mm/dd, or yyyy/mm or yyyy.
  --initial_path INITIAL_PATH
                        The initial url you want to crawl.
  --thread_num THREAD_NUM
                        The number of threads you want to use when crawling.
  --today, -t           Crawl the best images today
```

如：`python pixiv50_scraw_multi_thread.py --tp=2018/01`

`python pixiv50_scraw_multi_thread.py --initial_url='https://pic.tjsky.net/pixiv/pic/2019/'`

`python pixiv50_scraw_multi_thread.py --today`

### 注意！由于该网站并非每日及时更新，所以today选项很多时候会失效，最好是在月末直接爬取整个月份或直接指定时间段使用。

## 效果图

![](https://tva1.sinaimg.cn/large/006y8mN6ly1g6n9cvkb8yj30u01rind5.jpg)