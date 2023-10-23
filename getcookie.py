import time

from selenium import webdriver

from config import configs


def get_cookie():
    web_driver = webdriver.Chrome()

    web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')
    time.sleep(5)

    web_driver.find_element('xpath', '//*[@id="app"]/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[2]/button').click()
    time.sleep(5)
    dict_cookies = web_driver.get_cookies()
    print(dict_cookies)
    return dict_cookies


if __name__ == '__main__':
    get_cookie()
