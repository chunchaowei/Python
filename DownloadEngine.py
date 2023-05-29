#!/usr/local/env python3
# -*- coding: utf-8 -*-
# 使用Python，通过自动化来应用于工作与学习使用
# By Chunchao.Wei

import urllib.request
import json
import socket
import queue
import urllib.parse
import requests
from os import path
from PyQt5.QtCore import *
from PyQt5 import QtCore
from fake_useragent import UserAgent

global my_header
my_header = {'User-Agent': UserAgent().random,
             "Accept-Encoding": "gzip, deflate, br",
             "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
             "Connection": "keep-alive"}
global bad
bad = 0

class ImageDownloadThread(QThread):
    sub_progressBar_updated_signal = QtCore.pyqtSignal()

    def __init__(self, queue_in, dir_in):
        super(ImageDownloadThread, self).__init__()
        self.my_queue = queue_in
        self.dir = dir_in
        self.start()

    #使用队列实现进程间通信
    def run(self):
        while (True):
            global bad
            img_url = self.my_queue.get()
            # print(img_url)
            socket.setdefaulttimeout(5)    # 这里对整个socket层设置超时时间。后续连接中如果再使用到socket，不必再设置
            try:
                response = urllib.request.urlopen(img_url)
                # file_ext = path.splitext(img_url)[-1].split("?")[0]  # Extract the file extension
                file_name = f"image_{self.my_queue.qsize()}.jpg"  # Construct the file name with the extension
                file_path = path.join(self.dir, file_name)  # Combine the directory and file name
                with open(file_path, "wb") as f:
                    f.write(response.read())
            except Exception as e:
                print(f"-----{type(e)}: {img_url}-----\n")
            self.sub_progressBar_updated_signal.emit()    # 当使用者线程调用 task_done() 以表示检索了该项目、并完成了所有的工作时，那么未完成的任务的总数就会减少。
            if self.my_queue.empty():
                break
            self.my_queue.task_done()

class DownloadEngine(QThread):
    download_done_signal = QtCore.pyqtSignal(int)
    status_changed_signal = QtCore.pyqtSignal(str)
    progressBar_updated_signal = QtCore.pyqtSignal()

    def __init__(self, word_in, size_in, num_in, dir_in, thread_num_in):
        super(DownloadEngine, self).__init__()
        self.word = urllib.parse.quote(word_in)
        self.size = size_in
        self.num = num_in
        self.dir = dir_in
        self.thread_num = thread_num_in


    def ParseJSON(self, pn, rn, qe):
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&word=%s&pn=%d&rn=%d&z=%d'%(self.word, pn, rn, self.size)
        response = requests.get(url, headers=my_header)
        if response.status_code == 200:
            # json.loads将json字符串转化成python类型
            hjson = json.loads(response.content.decode())
            # print(hjson)
            for i in range(0, len(hjson['data']) - 1):  # 最后一个数据为空
                qe.put(hjson['data'][i]['thumbURL'])
                # print(qe)
                self.progressBar_updated_signal.emit()  # 更新进度条



    def GetImgUrlQueue(self):
        img_url_queue = queue.Queue(0)
        if self.num <= 30:
            self.ParseJSON(0, self.num, img_url_queue)    # 开始索引为0， 结束索引为self.num
        else:
            n = self.num / 30
            n = int(n)
            for i in range(n):
                start_index = i * 30
                self.ParseJSON(start_index, 30, img_url_queue)
            remaining_images = self.num - n * 30
            if remaining_images >0:
                start_index = n * 30
                self.ParseJSON(start_index, 30, img_url_queue)
        return img_url_queue

    def sub_update_progressBar(self):
        self.progressBar_updated_signal.emit()
        
    def run(self):
        global bad
        bad = 0
        self.status_changed_signal.emit('获取URL')
        img_url_queue = self.GetImgUrlQueue()
        threads = []
        self.status_changed_signal.emit('下载图片')
        #多线程爬去图片
        for i in range(self.thread_num):
            thread=ImageDownloadThread(img_url_queue, self.dir)
            thread.sub_progressBar_updated_signal.connect(self.sub_update_progressBar)
            threads.append(thread)
            thread.start()

        #合并进程，当子进程结束时，主进程才可以执行
        # Connect the finished signal of each thread to a lambda function that will remove the thread from the list
        for thread in threads:
            thread.finished.connect(lambda: threads.remove(thread))
            # print(thread)
        self.status_changed_signal.emit('下载完成')
        self.download_done_signal.emit(bad)

        # Wait until all the threads have finished
        while threads:
            QThread.sleep(1)  # Sleep briefly to avoid excessive CPU usage
