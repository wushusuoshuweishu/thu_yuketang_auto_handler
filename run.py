import time
import winsound
import sys

from selenium import webdriver

from config import configs


def auto_handle(mode, lesson_name):
    # setup the chrome driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.binary_location = configs['binary_location']
    web_driver = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=options)

    cookies = configs['cookie']

    web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')
    # WebDriver.get('https://yuketang.cn/')

    for cookie in cookies:
        web_driver.add_cookie(cookie)

    # login using cookie
    web_driver.refresh()
    time.sleep(5)
    # click "我的课程"
    web_driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div/div[2]/button').click()
    time.sleep(5)
    flag = 1
    while flag:
        try:
            # click "正在上课提醒"
            web_driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div[1]').click()
            lesson_infos = web_driver.find_elements_by_class_name('lessonTitle')
            for lesson in lesson_infos:
                if lesson.text == lesson_name:
                    # 成功发现该课程，发出440Hz、5s的蜂鸣提醒
                    web_driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div').click()
                    winsound.Beep(440, 5000)
                    flag = 0
            raise Exception
        except:
            # 否则刷新页面并等待5s
            web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')
            # WebDriver.get('https://yuketang.cn/')
            time.sleep(5)
            continue

    handles = web_driver.window_handles

    # 切换到最新打开的课程窗口
    web_driver.switch_to.window(handles[-1])
    iframe = web_driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/iframe')
    web_driver.switch_to.frame(iframe)

    # 手动答题模式
    while mode:
        try:
            # 每隔5s进行检测，发现有题后，发出1kHz、2s的蜂鸣提醒
            web_driver.find_element_by_class_name('page-exercise')
            winsound.Beep(1000, 2000)
            time.sleep(5)
        except:
            time.sleep(5)
            continue

    # 自动答题功能，
    while not mode:
        # 单选题/多选题
        try:
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/'
                                             'section/section/section[1]/section/section/section/section/p[1]').click()
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/section/'
                                             'section[1]/section/section/section/section/div[2]').click()
        except:
            pass
        # 主观题（有bug）
        try:
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/section/'
                                             'section[1]/section/div/section/section/div[2]').click()
            i = 1
            while web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/'
                                                   'section/section[1]/section/section/ul/li[' + str(i) + ']'):
                web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/section/'
                                                 'section[1]/section/section/ul/li[1]').send_keys('不会')
                i = i + 1
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/section/'
                                             'section[1]/section/section/div/p').click()
        except:
            pass
        # 忘了啥题，应该也是主观题的一种（显然也有问题，实在不行直接把屎山删了吧）
        try:
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/section/'
                                             'section[1]/section/section[1]/div/section/section/div[2]').click()
            web_driver.find_element_by_xpath(
                '//*[@id="app"]/section/section[1]/section[2]/section/section/section/section[1]/section/section[2]/'
                'section/div[2]/section[1]/textarea'
            ).send_keys('不会')
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/section/'
                                             'section[1]/section/section[2]/div/p').click()
        except:
            pass


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print("用法：python run.py [mode] [lesson_name]\n其中：\n    mode        0:自动答题\n                非0:提醒答题\n  "
              "  lesson_name 课程全名（注意区分课程名中的括号，有些是中文括号，有些是英文括号）")
    auto_handle(args[1], args[2])
