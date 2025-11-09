#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime as dt, timedelta
from itertools import permutations, combinations
from typing import List, Optional

from seleniumwire import webdriver

from constants import CHROME
from constants.setting import WHICH_DRIVER


def init_driver():
    """ 初始化浏览器配置信息 """
    # 创建一个配置对象, 默认使用EDGE
    options = webdriver.EdgeOptions() if WHICH_DRIVER.lower() != CHROME else webdriver.ChromeOptions()
    options.add_argument("--incognito")  # 隐身模式（无痕模式）
    # options.add_argument('--headless')  # 启用无头模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--pageLoadStrategy=eager")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--ignore-ssl-errors")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 不显示正在受自动化软件控制的提示
    # 如果需要指定Chrome驱动的路径，取消下面这行的注释并设置正确的路径
    # chromedriver_path = '/path/to/chromedriver'
    # 如果需要指定路径，可以加上executable_path参数
    if WHICH_DRIVER.lower() == CHROME:
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Edge(options=options)
    driver.maximize_window()

    return driver


def generate_flight_routes(crawl_citys: List[str], bidirectional: bool = True):
    """ 基于传入的城市列表，生成【起始城市 → 目的地城市】的组合。

    参数:
        crawl_citys: 城市列表，例如 ["深圳", "东京", "曼谷"]
        bidirectional: 是否生成双向组合。
            - True：生成双向组合（例如 深圳→东京、东京→深圳）
            - False：仅生成单向组合（例如 只保留 深圳→东京）

    返回: 所有城市组合对 (出发地, 目的地)，不包含相同城市。

    示例:
        >> gen_citys(["深圳", "东京", "曼谷"])
        [('深圳', '东京'), ('深圳', '曼谷'),
         ('东京', '深圳'), ('东京', '曼谷'),
         ('曼谷', '深圳'), ('曼谷', '东京')]

        >> gen_citys(["深圳", "东京", "曼谷"], bidirectional=False)
        [('深圳', '东京'), ('深圳', '曼谷'), ('东京', '曼谷')]
    """
    if bidirectional:
        return list(permutations(crawl_citys, 2))
    else:
        return list(combinations(crawl_citys, 2))


def generate_flight_dates(
        n: int,
        begin_date: Optional[str] = None,
        end_date: Optional[str] = None,
        start_interval: int = 1,
        days_interval: int = 1,
) -> List[str]:
    """
    根据指定条件生成一系列航班日期。

    可基于起始日期或相对当前日期的偏移量生成指定天数范围内的航班日期。
    若提供结束日期，则不会超过该日期。

    参数：
        n (int): 日期跨度天数，从起始日期开始计算。
        begin_date (str | None): 起始日期，格式 "YYYY-MM-DD"；若提供则优先使用。
        end_date (str | None): 结束日期，格式 "YYYY-MM-DD"，用于限制生成范围。
        start_interval (int): 若未指定 begin_date，则以当前日期加此偏移量作为起点。
        days_interval (int): 每隔多少天生成一个日期。

    返回：
        List[str]: 生成的日期字符串列表（格式："YYYY-MM-DD"）。

    示例：
        >> generate_flight_dates(10, begin_date="2025-05-01", days_interval=3)
        ['2025-05-01', '2025-05-04', '2025-05-07', '2025-05-10']
    """
    # 计算起始日期
    if begin_date:
        start_date = dt.strptime(begin_date, "%Y-%m-%d")
    else:
        start_date = dt.now() + timedelta(days=start_interval)

    # 如果提供了结束日期，则优先使用它来截断范围
    max_date = dt.strptime(end_date, "%Y-%m-%d") if end_date else None

    flight_dates = []
    current_date = start_date
    end_limit = start_date + timedelta(days=n)

    while current_date <= end_limit:
        if max_date and current_date > max_date:
            break
        flight_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=days_interval)

    return flight_dates


def element_to_be_clickable(element):
    """ 自定义 Selenium 等待条件函数
    替代 expected_conditions.element_to_be_clickable 或 expected_conditions.visibility_of_element_located
    """

    def check_clickable(driver):
        try:
            if element.is_enabled() and element.is_displayed():
                return element  # 当条件满足时，返回元素本身
            else:
                return False
        except (Exception,):
            return False

    return check_clickable
