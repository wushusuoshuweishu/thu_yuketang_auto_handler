import random
import time
import datetime
import winsound

from selenium import webdriver

from config import configs


def auto_handle(mode, lesson_name, default_options: list, default_content: str):
    # setup the chrome driver
    web_driver = webdriver.Chrome()

    cookies = configs['cookie']

    web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')

    print(str(datetime.datetime.now()) + "：启动成功")

    for cookie in cookies:
        web_driver.add_cookie(cookie)

    # login using cookie
    web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')
    time.sleep(5)
    flag = 1

    print(str(datetime.datetime.now()) + "：登录成功")

    while flag:
        try:
            # click "正在上课提醒"
            web_driver.find_element('xpath', '//*[@id="app"]/div[2]/div[2]/div[2]/div/div[1]/div[1]').click()
            lesson_infos = web_driver.find_elements('class name', 'lessonTitle')
            for lesson in lesson_infos:
                if lesson.text == lesson_name:
                    # 成功发现该课程，发出440Hz、2s的蜂鸣提醒
                    lesson.click()
                    winsound.Beep(440, 2000)
                    print(str(datetime.datetime.now()) + "：进入课程成功")
                    flag = 0
            raise Exception
        except:
            # 否则刷新页面并等待5s
            web_driver.get('https://tsinghua.yuketang.cn/pro/courselist')
            time.sleep(5)
            continue

    handles = web_driver.window_handles

    # 切换到最新打开的课程窗口及iframe
    web_driver.switch_to.window(handles[-1])
    iframe = web_driver.find_element('xpath', '//*[@id="app"]/div[2]/div[2]/div[2]/div/iframe')
    web_driver.switch_to.frame(iframe)

    # 手动答题模式
    while True:
        try:
            # 每隔5s进行检测，发现有题后，发出1kHz、2s的蜂鸣提醒
            web_driver.find_element('class name', 'page-exercise')
            if len(web_driver.find_elements('xpath', "//div[@class='timing' and contains(text(), '已完成')]")) != 0:
                # 该题已答，不用执行下列步骤
                raise Exception
            if len(web_driver.find_elements(
                    'xpath', "//div[contains(@class, 'timing willEnd') and text()='student.receivertimeout']")) != 0:
                # 该题已超时未答，不用执行下列步骤
                print(str(datetime.datetime.now()) + "：该题超时未答，当前模式--mode==" + str(mode))
                raise Exception
            print(str(datetime.datetime.now()) + "：发现题目")
            if str(mode) != "0":
                winsound.Beep(1000, 2000)
            else:
                elements_with_data_option = web_driver.find_elements('css selector', '[data-option]')
                if len(elements_with_data_option) > 0:
                    for element in elements_with_data_option:
                        data_option_value = element.get_attribute('data-option')
                        if default_options:
                            if data_option_value in default_options:
                                # 依次选择指定的选项
                                element.click()
                        else:
                            # default_options未指定，默认随机选
                            if random.randint(0, 1):
                                element.click()
                else:
                    # TODO: 主观题自动答题
                    pass
                web_driver.find_element("xpath", '//*[@id="app"]/section/section[1]/section[2]/section/section/section/section[1]/section/section/section/section/div[2]').click()
            time.sleep(5)
        except:
            time.sleep(5)
            continue


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default=0, help="运行模式，其中0为自动答题，非0为提醒答题")
    parser.add_argument("--name", type=str, default="", help="课程全名（注意区分课程名中的括号，有些是中文括号，有些是英文括号）")
    parser.add_argument("--options", type=str, default="", help="指定自动答题的选项，例如ABC（单选题则默认选字典序最大者C）。如不指定该参数且mode==0，则随机选项")

    args = parser.parse_args()
    auto_handle(args.mode, args.name, list(args.options), "")
