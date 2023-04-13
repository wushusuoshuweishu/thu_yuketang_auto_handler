# thu_yuketang_auto_handler

这是一个辅助清华大学学生应对荷塘雨课堂签到、发题的项目。

主要功能：

- 监测目标课程雨课堂上课提醒，并自动进入签到
  - 这一点可以用来专门针对那种上到一半才突然开雨课堂并发题的课（说的就是你！移动应用软件开发！）
  - 也可以帮助起不来的早八人~~早十人~~在上午仍然能够放心地获得婴儿一般的睡眠
- 进入课堂后，可以自动代答题，或者在监测到发题的时候发出蜂鸣提醒您
  - 您可以放心地将时间交给更加重要的事

不足之处：

- 暂时只支持单选题、多选题的自动代答（默认选A），不支持客观题自动代答，投票题暂未测试
- 使用了旧版的selenium库中的api，且该api已在最新版selenium库中被弃用
- 缺乏测试用户，可能存在隐含的bug
- 提醒答题模式下，只要停留在答题界面，就会每隔5s一直蜂鸣报警，或许会造成一定不适
- 或许可以支持更多选项的参数化，例如监测间隔、蜂鸣提示音等
- etc.

所以，欢迎各位清华大学的同学们一起贡献代码or使用意见，让我们不再被雨课堂束缚，去做更有意义的事！

### 环境配置

- 本项目仅测试了在windows 10，python3环境下的运行结果。
- 首先确认您安装了chrome浏览器，否则[下载](https://www.google.com/chrome/)。

- 之后，在chrome地址栏输入[chrome://version](chrome://version)。

- 在打开的界面中查看Google Chrome版本，然后[下载](https://chromedriver.chromium.org/downloads)对应版本的chromedriver，并将下载的压缩包解压后放在`drivers`路径下。
- 查看您的chrome浏览器的二进制文件路径。例如`C:\Program Files\Google\Chrome\Application\chrome.exe`，将该路径复制到`config.py`文件中的`'binary_location'`中。

- 运行`pip install -r requirements.txt`
  - 当然，我非常推荐您使用[虚拟环境](https://docs.python.org/3/library/venv.html)，以避免您环境中原有的selenium库版本受到本项目的影响。

### 使用方法

- 首先运行`python getcookie.py`，同时，您需要打开手机微信扫码，并对准屏幕中央，登录二维码将在命令执行后5秒出现。您需要在二维码出现后**5秒内**完成扫码，否则将无法获取正确cookie。
  - cookie将打印在控制台中，您需要将该cookie复制到`config.py`中的`cookie`中。
  - 这帮助您获取自己账号的cookie，使得在一段时间内不用再次扫码即可自动登录。
  - 我保证不会使用您的cookie，因为您的cookie只保存在本地
  - 运行期间注意不要人为点击

- 之后运行`python run.py [mode] [lesson_name]`，其中参数的含义分别为：
  - mode
    - 0：自动答题
    - 非0：提醒答题
  - lesson_name：需要监测的课程**全名**
    - 注意区分中英文括号
- 如果您在运行`run.py`时发现无法自动登录，则有可能是您未正确获取cookie，或cookie已失效。请您重新运行`getcookie.py`，并按要求操作。
- `run.py`成功运行后，每隔5秒刷新一次，查看您监测的课程是否开课。若开课，您将听到440Hz、长达5秒的蜂鸣提示。之后便进入监测答题/自动答题阶段
  - 此时您最好不要对该chrome窗口做任何操作，包括新增标签页、切换PPT等（您需要时刻保持PPT在教师正在放映的页面才能保证发题监测），否则，您将可能无法收到答题提醒，或无法自动答题。
  - 自动答题：
    - 单选题：自动选A并提交
    - 多选题：自动选A并提交
    - etc.：待支持
  - 提醒答题：
    - 发出1000Hz、长达2秒的蜂鸣提示
    - 仅测试了一般答题，对于“投票题”等不确定是否为“exercise”的题不确定能否正常提醒。

### 关于其他雨课堂...

我根据[aa5438a](https://github.com/wushusuoshuweishu/thu_yuketang_auto_handler/tree/aa5438a8ec92842b7d3a7879c99fac6f42565e9d)的`run.py`写了一份简单的[教学](./教学/README.md)，或许使用其他雨课堂的高校学生可以参考一下..?

### License

[GPL-3.0 license](./LICENSE)