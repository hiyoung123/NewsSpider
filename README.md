# NewsSpider
新闻爬虫，为了做 NLP 实验，从搜狐新闻、网易新闻和新浪新闻爬取每日滚动新闻。持续更新，后续添加其他网站的爬取代码，数据仅供学习研究，不做商业用途。

## 数据说明

一次能爬取到的数据有限，并且都是最新的，所以每天都可以进行增量爬取。

### 数据来源
* 搜狐新闻

  | Category |                             URL                              |
  | :------: | :----------------------------------------------------------: |
  |   时政   | http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&page={}&size=20 |
  |   国际   | http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1461&page={}&size=20 |
  |   财经   | http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1463&page={}&size=20 |
  |   财经   | http://v2.sohu.com/integration-api/mix/region/82?size=25&adapter=pc&page={} |
  |   科技   | http://v2.sohu.com/integration-api/mix/region/5676?size=25&adapter=pc&page={} |
  |   娱乐   | http://v2.sohu.com/integration-api/mix/region/131?size=25&adapter=pc&page={} |
  |   体育   | http://v2.sohu.com/integration-api/mix/region/4357?size=25&adapter=pc&page={} |
  |   体育   | http://v2.sohu.com/integration-api/mix/region/4302?size=25&adapter=pc&page={} |

* 新浪新闻

  | Category |                             URL                              |
  | :------: | :----------------------------------------------------------: |
  |   国内   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2510&k=&num=50&page=1 |
  |   国际   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2511&k=&num=50&page=1 |
  |   体育   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2512&k=&num=50&page=1 |
  |   娱乐   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2513&k=&num=50&page=1 |
  |   军事   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2514&k=&num=50&page=1 |
  |   科技   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&k=&num=50&page=1 |
  |   财经   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num=50&page=1 |
  |   股票   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2517&k=&num=50&page=1 |
  |   美股   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2518&k=&num=50&page=1 |
  |   社会   | https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2669&k=&num=50&page=1 |

* 网易新闻

  | Category |                             URL                              |
  | :------: | :----------------------------------------------------------: |
  |   要闻   |      https://temp.163.com/special/00804KVA/cm_yaowen.js      |
  |   国际   |      https://temp.163.com/special/00804KVA/cm_guoji.js       |
  |   国内   |      https://temp.163.com/special/00804KVA/cm_guonei.js      |
  |   体育   | https://sports.163.com/special/000587PR/newsdata_n_index.js  |
  |   NBA    |  https://sports.163.com/special/000587PR/newsdata_n_nba.js   |
  | 国际足球 | https://sports.163.com/special/000587PR/newsdata_n_world.js  |
  | 国内足球 | https://sports.163.com/special/000587PR/newsdata_n_china.js  |
  |   CBA    |  https://sports.163.com/special/000587PR/newsdata_n_cba.js   |
  |   综合   | https://sports.163.com/special/000587PR/newsdata_n_allsports.js |
  |   娱乐   |    https://ent.163.com/special/000380VU/newsdata_index.js    |
  |   明星   |    https://ent.163.com/special/000380VU/newsdata_star.js     |
  |   电影   |    https://ent.163.com/special/000380VU/newsdata_movie.js    |
  |  电视剧  |     https://ent.163.com/special/000380VU/newsdata_tv.js      |
  |   综艺   |    https://ent.163.com/special/000380VU/newsdata_show.js     |
  |   音乐   |    https://ent.163.com/special/000380VU/newsdata_music.js    |
  |   科技   |             http://tech.163.com/special/gd2016/              |
  |   财经   |  https://money.163.com/special/00259BVP/news_flow_index.js   |
  |   股票   |  https://money.163.com/special/00259BVP/news_flow_stock.js   |
  |   商业   |   https://money.163.com/special/00259BVP/news_flow_biz.js    |
  |   理财   |  https://money.163.com/special/00259BVP/news_flow_licai.js   |
  |   基金   |   https://money.163.com/special/00259BVP/news_flow_fund.js   |
  |   房产   |  https://money.163.com/special/00259BVP/news_flow_house.js   |
  |   汽车   |   https://money.163.com/special/00259BVP/news_flow_car.js    |

### 字段说明

|     字段      |   说明   |
| :-----------: | :------: |
|  news_title   | 新闻标题 |
| news_content  | 新闻内容 |
|   news_time   | 发布时间 |
|   news_site   | 新闻来源 |
| news_comments | 评论数量 |
|   news_type   | 新闻类型 |
|   news_link   | 新闻链接 |

## 使用说明

### 环境配置

```bash
pip install -r requirements.txt
```

### 代码执行

```bash
python main.py -s sohu -c 财经 -t 08-13 -f sohu.csv
```

### 参数说明

* -s：指定 spider，选项 [ sohu | sina | netease ]，没有默认值，必选项。
* -c：新闻类型，输入字符串，例如：财经、军事、娱乐等。默认值为 None，爬取全部类型新闻。
* -t：指定日期，输入格式 mm-dd，爬取指定日期的新闻。默认值为 None，爬取全部日期的新闻。
* -f：指定存储文件，必须是 CSV 后缀，存储路径为 NewsSpider/data，默认值为 news.csv。

## 代码说明

### pipelines

目前只有一个 NewsCSVPipeline ，用于将数据保存到 CSV 文件中。如有其他 pipelines 可以自己添加。

```python
class NewsCSVPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        self.file = open('NewsSpider/data/' + settings['EXPORTER_FILE'], 'wb')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True, encoding='utf-8')
        self.exporter.start_exporting()
        self.filter = BloomFilter()
        self.count = 0

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
          	# 使用 Bloom 过滤器，进行 URL 过滤，避免爬取重复 URL。
            if not self.filter.contains(item['news_link']):
                self.exporter.export_item(item)
                self.filter.insert(item['news_link'])
                self.count += 1
            else:
                print('{} 已经存在'.format(item['news_link']))
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        print('Saved user item size: {0}'.format(self.count))
```

### middlewares

中间价，目前只实现了 MyUserAgentMiddleware，用于随机使用 UserAgent，避免网站屏蔽，如需其他如 IPProxy 可自行实现。

```python
class MyUserAgentMiddleware:
    def __init__(self):
        self.user_agent_list = User_Agent

    def process_request(self, request, spider):
        request.headers['USER_AGENT'] = random.choice(self.user_agent_list)
```

### settings

配置文件，可进行爬虫配置，以及 log 配置。

```python
CONCURRENT_REQUESTS = 16 # 并行下载个数

DOWNLOAD_DELAY = 1 # 下载时间间隔

# log 配置
today = datetime.datetime.now()
log_file = 'NewsSpider/log/scrapy_{}_{}_{}.log'.format(today.year, today.month, today.day)
LOG_LEVEL = 'DEBUG'
LOG_FILE = log_file

```

### bloom

Bloom Filter，用于过滤重复 URL，避免重复下载。需要安装 Redis 数据库，并且配置好数据库信息。

## 参考

* https://github.com/ZRXXUAN/news-webscraping

