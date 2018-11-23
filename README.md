# 1993s spider
Crawl poster and mp4 from 1993s----从「在线之家」爬电影封面和视频<br/>
Join Telegram Group and contribute your idea！：https://t.me/joinchat/JG5m4hKWVamZJ_S9KldJFA

![image](https://raw.githubusercontent.com/Tsingtong/1993s/master/png/1.png)

## Features
+ High Speed video download architecture (up to 100Mbps)
+ Multi-threaded fetch multiple URLs
+ Easy install
+ Server Version is coming....

## 用法简介（从Docker）
+ Dockerfile is under development...

## 用法简介（从源码）

- ```本项目适用于py3，windows, mac, linux全平台支持```
- ```git clone https://github.com/Tsingtong/1993s.git ```
- ```cd 1993s && pip install -r requirements.txt```
- ```brew install phantomjs```
- ```cd 1993s && pip install -r requirements.txt```
- ```python crawler.py run movie_poster```
- 待程序运行完毕，会在movie_poster文件夹下download五页120个电影封面图，对应名称为：电影名_URL.jpg，如"蚁人2：黄蜂女现身_1567.jpg"
- 把URL放到download.txt里，运行```python crawler.py run mp4```, 在movie文件夹可看到下载好的该电影MP4文件
- ```python crawler.py run show_poster```
- 待程序运行完毕，会在show_poster文件夹下download五页120个美剧封面图，对应名称为：美剧名_URL.jpg，如"少年谢尔顿第二季_1528.jpg"
- 把URL放到download.txt里，运行```python crawler.py run mp4```, 在show文件夹可看到下载好的该美剧全集MP4文件


## 引用

- @[Pyflit](https://github.com/galeo/pyflit) is a simple Python HTTP downloader that support multi-thread downloading and multi-segment file downloading.
- @[Pornhub](https://github.com/formateddd/Pornhub) is a crawler that crawl webm and mp4
- @[selenium](https://github.com/SeleniumHQ/selenium) is a browser automation framework and ecosystem.
- @[PhantomJS](http://phantomjs.org/) is a headless web browser scriptable with JavaScript. It runs on Windows, macOS, Linux, and FreeBSD.

### Pyflit Features

+ HTTP GET
+ multi-threaded fetch multiple URLs
+ multi-segment file fetch
+ gzip/deflate/bzip2 compression supporting
+ a simple progress-bar
+ download pause and resume
+ proxy supporting

### Pornhub Features
+ crawl webm and mp4

### selenium Features
+ A browser automation framework and ecosystem.

### PhantomJS Features
+ PhantomJS is a headless web browser scriptable with JavaScript. It runs on Windows, macOS, Linux, and FreeBSD.
