#!/usr/bin/env python
# encoding: utf-8

# 爬取的城市
CRAWL_CITYS = ["香港", "东京"]

# 爬取日期范围：起始日期。格式'2023-12-01'
BEGIN_DATE = None

# 爬取日期范围：结束日期。格式'2023-12-31'
END_DATE = None

# 爬取T+N，即N天后
START_INTERVAL = 1

# 爬取的天数
CRAWL_DAYS = 60

# 设置各城市爬取的时间间隔（单位：秒）
CRAWL_INTERVAL = 5

# 日期间隔
DAYS_INTERVAL = 1

# 设置页面加载的最长等待时间（单位：秒）
MAX_WAIT_TIME = 10

# 最大错误重试次数
MAX_RETRY_TIME = 5

# 是否只抓取直飞信息（True: 只抓取直飞，False: 抓取所有航班）
DIRECT_FLIGHT = True

# 是否抓取航班舒适信息（True: 抓取，False: 不抓取）
COMFT_FLIGHT = False

# 是否删除不重要的信息
DEL_INFO = False

# 是否重命名DataFrame的列名
RENAME_COL = True

# 调试截图
ENABLE_SCREENSHOT = False

# 允许登录（可能必须要登录才能获取数据）
LOGIN_ALLOWED = True

# 账号
ACCOUNTS = ['', '']

# 密码
PASSWORDS = ['', '']

# 本地登录缓存
COOKIES_FILE = "cookies.json"
REQUIRED_COOKIES = ["AHeadUserInfo", "DUID", "IsNonUser", "_udl", "cticket", "login_type", "login_uid"]

# 后台运行模式
ENABLE_BACKEND = False

# 使用浏览器 edge or chrome
WHICH_DRIVER = "edge"

# chrome驱动路径
CHROME_DRIVER_PATH = None
