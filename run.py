import time
import datetime
import winsound

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

    print(str(datetime.datetime.now()) + "：启动成功")

    for cookie in cookies:
        web_driver.add_cookie(cookie)

    # login using cookie
    web_driver.refresh()
    time.sleep(5)
    # click "我的课程"
    web_driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div/div[2]/button').click()
    time.sleep(5)
    flag = 1

    print(str(datetime.datetime.now()) + "：登录成功")

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
                    print(str(datetime.datetime.now()) + "：进入课程成功")
                    flag = 0
            raise Exception
        except:
            # 否则刷新页面并等待5s
            web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')
            # WebDriver.get('https://yuketang.cn/')
            time.sleep(5)
            continue

    handles = web_driver.window_handles

    # 切换到最新打开的课程窗口及iframe
    web_driver.switch_to.window(handles[-1])
    iframe = web_driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/iframe')
    web_driver.switch_to.frame(iframe)

    # 手动答题模式
    while str(mode) != "0":
        try:
            # 每隔5s进行检测，发现有题后，发出1kHz、2s的蜂鸣提醒
            web_driver.find_element_by_class_name('page-exercise')
            print(str(datetime.datetime.now()) + "：发现题目")
            winsound.Beep(1000, 2000)
            time.sleep(5)
        except:
            time.sleep(5)
            continue

    # 自动答题功能，
    while str(mode) == '0':
        # 单选题/多选题
        try:
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/'
                                             'section/section/section[1]/section/section/section/section/p[1]').click()
            web_driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/section[2]/section/section/section/'
                                             'section[1]/section/section/section/section/div[2]').click()
            print(str(datetime.datetime.now()) + "：选择题自动答题成功")
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
            print(str(datetime.datetime.now()) + "：主观题自动答题成功")
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
            print(str(datetime.datetime.now()) + "：主观题自动答题成功")
        except:
            pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default=0, help="运行模式，其中0为自动答题，非0为提醒答题")
    parser.add_argument("--name", type=str, default="", help="课程全名（注意区分课程名中的括号，有些是中文括号，有些是英文括号）")

    args = parser.parse_args()
    auto_handle(args.mode, args.name)
