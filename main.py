#!/usr/bin/env python
# encoding: utf-8

from core.crawler import *
from core.utils import init_driver, generate_flight_routes, generate_flight_dates


def ctrip_crawler_runner():
    driver = init_driver()

    cities = generate_flight_routes(CRAWL_CITYS)

    flight_dates = generate_flight_dates(CRAWL_DAYS, BEGIN_DATE, END_DATE, START_INTERVAL, DAYS_INTERVAL)

    flight_data_fetcher = DataFetcher(driver)

    for city in cities:
        flight_data_fetcher.city = city

        for flight_date in flight_dates:
            flight_data_fetcher.date = flight_date

            if os.path.exists(
                    os.path.join(os.getcwd(), flight_date, dt.now().strftime("%Y-%m-%d"), f"{city[0]}-{city[1]}.csv")):
                print(
                    f'{time.strftime("%Y-%m-%d_%H-%M-%S")} 文件已存在:{os.path.join(os.getcwd(), flight_date, dt.now().strftime("%Y-%m-%d"), f"{city[0]}-{city[1]}.csv")}')
                continue
            elif 'http' not in flight_data_fetcher.driver.current_url:
                print(f'{time.strftime("%Y-%m-%d_%H-%M-%S")} 当前的URL是：{driver.current_url}')
                # 初始化页面
                flight_data_fetcher.get_page(1)

            else:
                # 后续运行只需更换出发与目的地
                flight_data_fetcher.change_city()

            time.sleep(CRAWL_INTERVAL)

    # 运行结束退出
    try:
        driver = flight_data_fetcher.driver
        driver.quit()
    except Exception as e:
        print(f'{time.strftime("%Y-%m-%d_%H-%M-%S")} An error occurred while quitting the driver: {e}')

    print(f'\n{time.strftime("%Y-%m-%d_%H-%M-%S")} 程序运行完成！！！！')


if __name__ == '__main__':
    ctrip_crawler_runner()
