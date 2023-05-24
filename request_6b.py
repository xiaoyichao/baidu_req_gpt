#!/usr/bin/python #-*- coding:utf8 -*-
################################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
# Power by gaoming06 2023-01-17 19:21:15
# File: request.py
# Description: 
"""

import sys
import traceback
import requests
import json
import numpy as np
import os
import urllib
import time
import random
import subprocess
import ssl


class ReqGPT(object):
    """
    """
    def __init__(self):
        """
        初始化
        """
        # chatGPT线上服务地址
        self.vec_server_list = self.get_bns_server("group.aigcgpu-aigcchatglm6b.AIGC-GPU.all")

        random_server = random.choice(self.vec_server_list)
        self.ip, self.port = random_server[0], random_server[1]

        # 重试次数
        self.retry_times = 3
        # 设置ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_bns_server(self, bns_name):
        """
        Summary: 通过bns获取ip port

        Args:
            bns_name: bns

        Returns:
        """
        try:
            result = []
            cmd = "get_instance_by_service -a %s | awk '{if($5==0){print $2,$4}}'" % bns_name
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            for line in popen.stdout.readlines():
                line = line.decode('utf-8')
                host, port = line.strip('\n').split()
                result.append((str(host), str(port)))
            return result
        except:
            # traceback.print_exc()
            return []


    def run(self, text):
        """
        主控流程

        Args:

        Returns:

        """
        try:
            # 请求gpt
            res = self.req_gpt(text)
        except Exception as ex:
            # print (str(ex))
            return False

    def req_gpt(self, text):
        """
        请求open-ai gpt

        Args:

        Returns:

        """
        try:

            sixb_url = "http://{}:{}".format(self.ip, self.port)
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "prompt": text, #"请仔细阅读以下内容，帮大家进行信息抽取：\n{}\n从上述内容中总结一个100-300字并且能够概括文章核心思想的问题和回答\n".format(text)
                "temperature":0,
                "top_p":0.8,
            }
            res = self.urllib_request(sixb_url, json.dumps(data), headers)
            #print("res", res)
            # 重试机制
            retry = 0
            while (res is None) and (retry < self.retry_times):
                res = self.urllib_request(sixb_url, json.dumps(data), headers=headers)
                retry += 1
            if res is None:
                return False
            ret = json.loads(res)
            return ret
        except Exception as ex:
            # print ("request cut url fail with exception [%s]" % (str(ex)))
            return False

    def urllib_request(self, param_url, param_data="", headers={}):
        """
        Summary:使用urllib发送请求

        Args:
            param_url: url地址
            param_data: 请求数据
        Returns:
        """
        rsp = None
        try:
            if param_data:
                if type(param_data) != bytes:
                    param_data_b = param_data.encode('utf-8')
                    req = urllib.request.Request(param_url, data=param_data_b, headers=headers)
                else:
                    req = urllib.request.Request(param_url, data=param_data, headers=headers)
            else:
                req = urllib.request.Request(param_url, headers=headers)
            rsp = urllib.request.urlopen(req, timeout=60)
            rsp = rsp.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            # print (str(e))
            return None
        # print (rsp)
        return rsp

if __name__ == "__main__":
    obj = ReqGPT()
    cnt = 0
    import sys
    import json
    from time import time
    input_file = open(sys.argv[1])
    # for index, line in enumerate(input_file):
    #     if index < 10:
    #         continue
        # parts = line.strip('\n').split("\t")
        # content = parts[0].split(":")[-1]
        # prompt = content

    # prompt = "回答以下问题：\n{}".format(content) #nlu-推理任务
    # prompt = "将下面句子翻译成中文：\n{}".format(content.replace("+", " ")) #nlu-机器翻译
    # prompt = "请根据以上内容生成10字以内的标题: \n{}".format(content) #nlu-摘要提取
    # prompt = "缩写下面内容 \n{}".format("第一次出门打工的经历令人感动。") #nlu-摘要提取
    
    # print(prompt)
    prompt = "AI 写作助手 \n{}".format("官渡之战介绍") #nlu-摘要提取

    res = obj.req_gpt(prompt)
    # if res is False:
    #     continue
    t2 = time()
    res_6b = res.get("response", "")
    print("{}".format(res_6b) )
    # print("{}\t{}".format(parts[0], res_6b)) #replace('\t', '').replace("\n", "").replace("\r", "")



        
