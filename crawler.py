#!/usr/bin/env python
# coding=utf-8

import os
import urllib
import json
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pyflit import flit

import gevent
import requests
from lxml import etree
import fire
from dumblog import dlog
logger = dlog(__file__)


def list_page(url, foldername):
    logger.info('crawling : %s' % url)
    driver = webdriver.PhantomJS()
    driver.set_window_size(1366, 768)
    driver.get(url)
    resp = driver.page_source
    html = etree.HTML(resp)
    driver.close()
    driver.quit()

    vkeys = html.xpath('//*[@class="stui-vodlist__thumb lazyload"]/@href')
    vjpgs = html.xpath('//*[@class="stui-vodlist__thumb lazyload"]/@data-original')
    vtitles = html.xpath('//*[@class="stui-vodlist__thumb lazyload"]/@title')

    jobs = []
    for i in range(len(vkeys)):
        item = {}
        vkeytemp = vkeys[i].split('/')[-1]
        vkeytemp = vkeytemp.strip('.html')
        item['vname'] = vtitles[i] + '_' + vkeytemp
        item['vjpg'] = vjpgs[i]
        try:
            jobs.append(gevent.spawn(download_jpg, item['vjpg'], item['vname'], 'jpg', foldername))
        except Exception as err:
            logger.error(err)
    gevent.joinall(jobs, timeout=2)


def detail_page(url):
    chrome_options = Options()
    # 无头模式启动
    chrome_options.add_argument('--headless')
    # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--disable-gpu')
    # 初始化实例
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    resp = driver.page_source
    html = etree.HTML(resp)


    # 获取视频名称
    title = ''.join(html.xpath('//h3[@class="title"]//text()')[0]).strip()
    # 获取视频链接
    try:
        vlists = html.xpath('//ul[@class="stui-content__playlist clearfix"]/li/a/@href')[0]
        vlists = 'http://www.1993s.top' + vlists
        video_class = 1
        foldername = 'movie'
    except IndexError:
        # vlists = html.xpath('//ul[@class="stui-content__playlist column10 clearfix"]/li/a/@href')[0]
        vlists = html.xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li/a/@href')
        for i in range(len(vlists)):
            vlists[i] = 'http://www.1993s.top' + vlists[i]
        video_class = 2
        foldername = 'show'
    vjs = []
    # 切换到视频框frame
    if video_class == 1:
        driver.get(vlists)
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
        resp = driver.page_source
        html = etree.HTML(resp)
        vjs.append(html.xpath('//*[@class="dplayer-video dplayer-video-current"]/@src'))
        print(vjs)
    else:
        for i in range(len(vlists)):
            driver.get(vlists[i])
            driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
            resp = driver.page_source
            html = etree.HTML(resp)
            vjs.append(html.xpath('//*[@class="dplayer-video dplayer-video-current"]/@src'))
            print(vjs[i])
    driver.close()
    # driver.quit()

    for num, video in enumerate(vjs):
        logger.info('downloading: %s', video)
        try:
            download_mp4(video[0], str(title+'_'+str(num+1)), 'mp4', foldername)
        except Exception as err:
            logger.error(err)


def download_jpg(url, name, filetype, foldername):
    filepath = '%s/%s.%s' % (foldername, name, filetype)
    if os.path.exists(filepath):
        logger.warn('this file had been downloaded :: %s' % (filepath))
        return
    urllib.request.urlretrieve(url, '%s' % (filepath))
    logger.info('download success :: %s' % (filepath))


def download_mp4(url, name, filetype, foldername):
    filepath = '%s/%s.%s' % (foldername, name, filetype)
    # if os.path.exists(filepath):
    #     logger.warn('this file had been downloaded :: %s' % (filepath))
    #     return:
    name = name.rstrip('_1234567890')
    os.chdir(foldername)
    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)
    # urllib.request.urlretrieve(url, '%s' % (filepath))
    segment_number = 64
    opener = flit.get_opener()
    flit.flit_segments(url, segment_number, opener)
    os.chdir("../..")
    logger.info('download success :: %s' % (filepath))


def run(_arg=None):
    paths = ['movie', 'show', 'movie_poster', 'show_poster']
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)
    if _arg == 'movie_poster':
        urls = [
            'http://www.1993s.top/list/1.html',
            'http://www.1993s.top/list/1-2.html',
            'http://www.1993s.top/list/1-3.html',
            'http://www.1993s.top/list/1-4.html',
            'http://www.1993s.top/list/1-5.html'
        ]
        jobs = [gevent.spawn(list_page, url, 'movie_poster') for url in urls]
        gevent.joinall(jobs)
    elif _arg == 'show_poster':
        urls = [
            'http://www.1993s.top/list/2.html',
            'http://www.1993s.top/list/2-2.html',
            'http://www.1993s.top/list/2-3.html',
            'http://www.1993s.top/list/2-4.html',
            'http://www.1993s.top/list/2-5.html'
        ]
        jobs = [gevent.spawn(list_page, url,'show_poster') for url in urls]
        gevent.joinall(jobs)
    elif _arg == 'mp4':
        with open('download.txt', 'r') as file:
            keys = list(set(file.readlines()))
        jobs = []
        for key in keys:
            url = 'http://www.1993s.top/detail/%s' % key.strip()
            logger.info(url)
            jobs.append(gevent.spawn(detail_page, url))
        gevent.joinall(jobs, timeout=2)
    else:
        _str = """
tips:
    python crawler.py run movie_poster
        - 下载120部热门电影的缩略图，路径为movie_poster文件夹下
        
    python crawler.py run show_poster
        - 下载120部热门美剧的缩略图，路径为show_poster文件夹下

    python crawler.py run mp4
        - 将下载的jpg文件对应的以_之后的文件名逐行写在download.txt中，如：1677，运行该命令
        """
        logger.info(_str)
    logger.info('finish !')


if __name__ == '__main__':
    fire.Fire()
