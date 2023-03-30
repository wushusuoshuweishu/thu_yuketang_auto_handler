import time

from selenium import webdriver

from config import configs


def get_cookie():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.binary_location = configs['binary_location']
    web_driver = webdriver.Chrome(
        'drivers/chromedriver.exe', chrome_options=options)

    web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')  # 荷塘雨课堂
    # WebDriver.get('https://yuketang.cn/')
    time.sleep(5)

    web_driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div/div[2]/button').click()  # 荷塘雨课堂
    # WebDriver.find_element_by_xpath('//*[@id="nav"]/div[2]/a[3]').click()  # 雨课堂
    time.sleep(5)
    dict_cookies = web_driver.get_cookies()
    print(dict_cookies)
    return dict_cookies


if __name__ == '__main__':
    get_cookie()
