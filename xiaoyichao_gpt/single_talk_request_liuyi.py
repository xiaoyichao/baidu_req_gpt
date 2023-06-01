"""req_wenxin pub
- [ ] 根据pid看程序名称
ps -aux | grep 37540
- [ ] 根据程序名称 查询piddu -sh *
ps -ef|grep single_talk_request_2


    
log2
    nohup  python  xiaoyichao_gpt/single_talk_request_liuyi.py --bot_type glm130b  --task retie > "./logs_liuyi/glm130b_retie_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type glm6b --task retie > "./logs2/glm6b_retie_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type yiyan --task retie > "./logs2/yiyan_retie_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type minimax --task retie > "./logs2/minimax_retie_$(date +"%Y-%m-%d-%H").log" 2>&1 &

    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type glm130b  --task qunliao > "./logs2/glm130b_qunliao_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type glm6b --task qunliao > "./logs2/glm6b_qunliao_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type yiyan --task qunliao > "./logs2/yiyan_qunliao_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type minimax --task qunliao > "./logs2/minimax_qunliao_$(date +"%Y-%m-%d-%H").log" 2>&1 &

    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type glm130b  --task chuangzuozhe > "./logs2/glm130b_chuangzuozhe_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type glm6b --task chuangzuozhe > "./logs2/glm6b_chuangzuozhe_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type yiyan --task chuangzuozhe > "./logs2/yiyan_chuangzuozhe_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup  python  xiaoyichao_gpt/single_talk_request_2.py --bot_type minimax --task chuangzuozhe > "./logs2/minimax_chuangzuozhe_$(date +"%Y-%m-%d-%H").log" 2>&1 &


    nohup python  xiaoyichao_gpt/single_talk_request_liuyi.py --bot_type glm130b  --task rensheduihua > "./logs_liuyi/glm130b_rensheduihua_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup python  xiaoyichao_gpt/single_talk_request_liuyi.py --bot_type glm6b  --task rensheduihua > "./logs_liuyi/glm6b_rensheduihua_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup python  xiaoyichao_gpt/single_talk_request_liuyi.py --bot_type yiyan  --task rensheduihua > "./logs_liuyi/yiyan_rensheduihua_$(date +"%Y-%m-%d-%H").log" 2>&1 &
    nohup python  xiaoyichao_gpt/single_talk_request_liuyi.py --bot_type minimax  --task rensheduihua > "./logs/minimax_rensheduihua_$(date +"%Y-%m-%d-%H").log" 2>&1 &
"""
#!/usr/bin/env python
#-*- coding=utf8 -*-
import requests
import os
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import json
# import bns
import ssl
import argparse
import io
import time
import random
import subprocess
import subprocess
# import urllib
import traceback
from tqdm import tqdm
PYTHON3 = False if sys.version_info < (3, 0) else True
if not PYTHON3:
    import urllib2
else:
    import urllib.request as urllib2
import pandas as pd
# from requests_toolbelt import MultipartEncoder



def get_bns_server(bns_name):
    """
    Summary: 通过bns获取ip port

    Args:
        bns_name: bns

    Returns:
    """
    try:
        
        result = []
        try_num = 0
        while len(result)==0 and try_num<20:
            cmd = "get_instance_by_service -a %s | awk '{if($5==0){print $2,$4}}'" % bns_name
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            for line in popen.stdout.readlines():
                line = line.decode('utf-8')
                host, port = line.strip('\n').split()
                result.append((str(host), str(port)))
            try_num += 1
            time.sleep(2)
        
        return result
    except:
        return []

def urllib_request(param_url, param_data="", headers={}):
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
                req = urllib2.Request(param_url, data=param_data_b, headers=headers)
            else:
                req = urllib2.Request(param_url, data=param_data, headers=headers)

        else:
            req = urllib2.Request(param_url, headers=headers)
        rsp = urllib2.urlopen(req, timeout=60)
        rsp = rsp.read().decode('utf-8')

    except:
        # print(traceback.format_exc())
        return None

    return rsp

class ReqWenxin(object):
    """ReqWenxin"""
    def __init__(self):
        self.acdata = 'access_token.dat'
        self.boturl = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions'
        self.ckurl = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'
        self.appid = '32663422'
        self.ak = 'oehqUFEQKDw0Hbke3gy6KoPU'
        self.sk = 'yILXd7ZrXVBbacOKiZbOYxxtKkVBhOQy'
        self.retry_times = 3

    def gen_acckey(self):
        """gen_acckey"""
        url = '%s&client_id=%s&client_secret=%s' % (self.ckurl, self.ak, self.sk)
        res = requests.get(url)
        with open(self.acdata, 'w') as to:
            res_data = res.json()
            res_data['create_time'] = int(time.time())
            to.write(json.dumps(res_data))

    def read_acckey(self):
        """read_acckey"""
        ntime = int(time.time())
        with open(self.acdata, 'r') as tf:
            res_data = json.loads(tf.read())
            ctime = int(res_data['create_time'])
            etime = ctime + int(res_data['expires_in'])
            if ntime >= etime:
                return None
            return res_data['access_token']

    def req_bot(self, query):
        """req_bot"""
        try_num = 0
        ac = self.read_acckey()
        if ac is None:
            self.gen_acckey()
            ac = self.read_acckey()
        boturl='%s?access_token=%s' % (self.boturl, ac)

        reqdata = {"messages":[{"role":"user", "content":query}]}
        headers = {"Content-Type": "application/json"}
        bns_list = get_bns_server("group.iknow-llm-proxy-tpl-online.iknow.all")
        while len(bns_list)==0 and try_num<100:
            bns_list = get_bns_server("group.iknow-llm-proxy-tpl-online.iknow.all")
            time.sleep(random.randint(1,10))
        if len(bns_list)>0:
            random_server = random.choice(bns_list)
        self.ip, self.port = random_server[0], random_server[1]
        try:
            boturl='%s?access_token=%s'%(self.boturl, ac)
            res = requests.post(url=boturl, data=json.dumps(reqdata), headers = headers, timeout=120)
            retry = 1
            while (res is None) and (retry < self.retry_times):
                res = requests.post(url=boturl, data=json.dumps(reqdata), headers = headers, timeout=120)
                retry += 1

            res_data = res.json()
            res_data['query'] = query
            return (res_data)
        except:
            # print(traceback.format_exc())
            try:
                res = requests.post(url=boturl, data=json.dumps(reqdata), headers = headers, timeout=120)
                res_data = res.json()
                res_data['query'] = query
                return (res_data)
            except:
                return {}
            return {}

class ReqGLM_130b(object):
    """
    """
    def __init__(self):
        """
        初始化
        """
        # chatGPT线上服务地址
        self.vec_server_list = get_bns_server("group.iknow-llm-proxy-tpl-online.iknow.all")
        random_server = random.choice(self.vec_server_list)
        self.ip, self.port = random_server[0], random_server[1]

        # 重试次数
        self.retry_times = 3
        # 设置ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    def req_gpt(self, text):
        """
        请求open-ai gpt
        Args:
        Returns:
        """
        try:

            sixb_url = "http://{}:{}/api/paas/model/v1/open/engines/chatGLM/chatGLM".format(self.ip, self.port)
            headers = {
                "Content-Type": "application/json",
                'api-key': 'test-debug',
                'from': 'test'
            }
            data = {
                "prompt": text, #"请仔细阅读以下内容，帮大家进行信息抽取：\n{}\n从上述内容中总结一个100-300字并且能够概括文章核心思想的问题和回答\n".format(text)
                "temperature":0.9,
                "top_p":0.7
            }
            res = urllib_request(sixb_url, json.dumps(data), headers)
            # 重试机制
            retry = 1
            while (res is None) and (retry < self.retry_times):
                res = urllib_request(sixb_url, json.dumps(data), headers=headers)
                retry += 1
            if res is None:
                return False
            ret = json.loads(res)
            # print(ret)
            res_130b = ret.get("data", {}).get("outputText", "-1")
            return res_130b
        except Exception as ex:
            # print(traceback.format_exc())
            return "-1"



class RequestGPT4(object):

    def __init__(self):
        self.args = args

        self.deployment_id = "deploy_gpt4" #self.args.deployment_id
        self.api_version = '2023-03-15-preview'
        self.retry_times = 3
        bns_list = get_bns_server("group.iknow-llm-proxy-tpl-online.iknow.all")
        random_server = random.choice(bns_list)
        self.ip, self.port = random_server[0], random_server[1]
        self.openai_url = 'http://{}:{}/openai/deployments/{}/chat/completions?api-version={}'.format(self.ip, self.port, self.deployment_id, self.api_version)#self.api_version)

    def send_request_openai(self, prompt):
        """
            请求api
            param:
                request_data: 请求URL
            return:
                openai_result：openai返回结果
        """
        if prompt == '' or prompt == None:
            return '-1'
    
        user_prompt = prompt
        qa_info_dict = user_prompt
        request_data = json.dumps(qa_info_dict)
        # 请求头
        headers = {
                    'Content-Type': 'application/json',
                    'api-key': 'bot-c7db87e646f6b1fc8a80c213fd862809'
                  }
        try:
            web_response = urllib_request(self.openai_url, request_data, headers)
            retry = 1
            while (web_response is None) and (retry < self.retry_times):
                web_response = urllib_request(self.openai_url, request_data, headers)
                retry += 1
            if web_response is None:
                return '-1' 
            ret = json.loads(web_response)
            return_result = ret.get("choices", [{}])[0].get("message", {}).get("content", "-1")
        except:
            return_result = '-1'
            pass
        return return_result

class RequestGPT35(object):
    """
    RequestGPT35
    """
    def __init__(self):
        self.deployment_id = 'deploy_gpt35_turbo'
        self.api_version = '2023-03-15-preview'
        self.retry_times = 3
        bns_list = get_bns_server("group.iknow-llm-proxy-tpl-online.iknow.all")
        random_server = random.choice(bns_list)
        self.ip, self.port = random_server[0], random_server[1]
        self.openai_url = 'http://{}:{}/openai/deployments/{}/completions?api-version={}'.format(self.ip, self.port, self.deployment_id, self.api_version)
    def send_request_openai(self, prompt):
        """
        send_request_openai
        """
        user_prompt = prompt
        qa_info_dict = {
            "prompt": user_prompt,
            "max_tokens":4096,
            "temperature":0,
            "top_p":0.8,
            "frequency_penalty":0,
            "presence_penalty":0,
            "stop":["<|im_end|>"]
        }

        request_data = json.dumps(qa_info_dict)
        headers = {
                    'Content-Type': 'application/json',
                    'api-key': 'test-debug'
                  }
        try:
            web_response = urllib_request(self.openai_url, request_data, headers)
            # print(web_response)
            retry = 1
            while (web_response is None) and (retry < self.retry_times):
                web_response = urllib_request(self.openai_url, request_data, headers)
                retry += 1
            if web_response is None:
                return '-1' 
            ret = json.loads(web_response)
            return_result = ret.get("choices", [{}])[0].get("text", "")

        except:
            return_result = '-1'
            pass
        return return_result

class ReqGLM_6b(object):
    """
    ReqGLM_6b
    """
    def __init__(self):
        """
        初始化
        """

        self.vec_server_list = get_bns_server("group.aigcgpu-aigcchatglm6b.AIGC-GPU.all")
        random_server = random.choice(self.vec_server_list)
        self.ip, self.port = random_server[0], random_server[1]

        # 重试次数
        self.retry_times = 3
        # 设置ssl
        ssl._create_default_https_context = ssl._create_unverified_context
    def req_6b(self, text):
        """
        req_6b
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
            res = urllib_request(sixb_url, json.dumps(data), headers)
            retry = 0
            while (res is None) and (retry < self.retry_times):
                res = urllib_request(sixb_url, json.dumps(data), headers=headers)
                retry += 1
            if res is None:
                return "-1"
            ret = json.loads(res)
            res_6b = ret.get("response", "-1")
            return res_6b
        except Exception as ex:
            return "-1"


class Req_minimax(object):
    """
    Req_minimax
    """
    def __init__(self):
        """
        初始化
        """
        # 重试次数
        self.retry_times = 5
        self.group_id = "1684120827778191"
        self.api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoiMTExIiwiU3ViamVjdElEIjoiMTY4NDEyMDgyNzkwNjk4NSIsIlBob25lIjoiTVRNME9EZzRPVFl3TURZPSIsIkdyb3VwSUQiOiIxNjg0MTIwODI3Nzc4MTkxIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoibG91Y2hhbzAyQGJhaWR1LmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDIzLTA1LTI2IDEwOjIxOjUwIiwiaXNzIjoibWluaW1heCJ9.IMtDaL8mNwu-8wMznQgBsDzBfItyuKQp8S7IVsK-TV9x8PrLUSOLTACMvJibTL1s7R34yJAnpKxdTReTD_GRKMkCsfN1ThiFSHCwh2AG6TnvQ8yuUAIOeZKRszyuwfH3wpTV2a3XUkrCyoEOvXIYHFSl24GwzrtGhsU-Xdee6xveK-pyA5iMhAQoAh-9gV6IYRnbEC42rGnOV8QwSK-IQfRm_EiTF-1iKkFKBTZIFhU2uDNCRQ_fwO8vCXKFHih5saYp0WZFGBxbiJh0IILprtySZnBxb5V2FCy14VmrxqBPTH5rCoTvzDTs_UVyYaxmGw5lEpLgiXtWGA-oQxvdMA"
        self.url = f'https://api.minimax.chat/v1/text/chatcompletion?GroupId={self.group_id}'
    
    
    def req_minimax(self, text):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        request_body = {
            "model": "abab5-chat",
            "tokens_to_generate": 2048,
            'messages': []
        }

        res = []
        retry = 0
        reply = ""
        try:
            request_body['messages'].append({"sender_type": "USER", "text": text})
            while retry <= self.retry_times and not reply:
                response = requests.post(self.url, headers=headers, json=request_body)
                reply = response.json()['reply']
                if reply != "": 
                    time.sleep(10)
                else:
                    time.sleep(20)
                    print("请求接口失败", response._content, retry)
                retry += 1
            return reply
        except:
            print(traceback.format_exc(),"尝试多次后还是失败了", retry)
            return "-1"
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()



    parser.add_argument('--bot_type', default='minimax', type=str, choices=['yiyan', 'gpt4', 'gpt3.5', 'glm130b', "glm6b", "minimax"])
    parser.add_argument('--task', 
                        type=str,
                        default='rensheduihua')
    args = parser.parse_args()
    
    print("bot_type:{}".format(args.bot_type))

    if args.task == "retie":
        json_path = "xiaoyichao_gpt/prompt4retie.json"
        sheet_name = u"帖子总结"
    elif args.task == "qunliao":
        json_path = "xiaoyichao_gpt/prompt4qunliao.json"
        sheet_name = u"群聊内容总结"
    elif args.task == "chuangzuozhe":
        json_path = "xiaoyichao_gpt/prompt4chuangzuozhe.json"
        sheet_name = u"创作者内容二次加工"
    elif args.task == "rensheduihua":
        json_path = "xiaoyichao_gpt/prompt4rensheduihua.json"
        sheet_name = u"人设设定"


    with open(json_path, "r", encoding='utf8') as f:
        json_data = json.load(f)
        ori_prompt = json_data[args.bot_type]["prompt"]

    # ori_prompt = "你现在扮演的角色是{}贴吧用户。你收到了一个帖子，其内容如下：\n[{}]\n作为{}贴吧用户，你如何回复这篇帖子？"


    # 加载数据
    input_list = []
    res_list = []
    xlsx = pd.read_excel('人设对话-0.xlsx', sheet_name=sheet_name)
    # xlsx = pd.read_excel(args.input_file_path, sheet_name="知识增强") #输入
    # for i in range(len(xlsx.values)):
    # for i in tqdm(range(len(xlsx.values))):
    for i in tqdm(range(0, 210, 1)):
        # if i<2:
        #     continue
        ori_content = xlsx.values[i][1]
        ori_source = xlsx.values[i][0]

        # input_list.append(ori_content)

        # content = "```" + ori_content + "```"
        content =  ori_content 

        if args.bot_type == "yiyan": # 请求wenxin
            req_wenxin_api = ReqWenxin()
            prompt = ori_prompt+content
            prompt = ori_prompt.format(ori_source,ori_content,ori_source)


            res = req_wenxin_api.req_bot(prompt)
            res_wenxin = res.get("result", "-1")
            res_list.append(res_wenxin)
            print("wenxin_res:{}".format(res_wenxin))
            time.sleep(3)
        
        elif args.bot_type == "gpt4": # 请求gpt4
            req_gpt4_api = RequestGPT4()
            prompt_gpt = {"messages":[{"role":"user", "content":prompt}]}
            res_gpt = req_gpt4_api.send_request_openai(prompt_gpt)
            res_list.append(res_gpt)
            print("gpt4_res:{}".format(res_gpt))
            time.sleep(3)

        elif args.bot_type == "gpt35":  # 请求gpt35
            req_gpt35_api = RequestGPT35()
            prompt = "<|im_start|>user\n" + prompt + "\n<|im_end|>\n"
            openai_result = req_gpt35_api.send_request_openai(prompt)
            res_list.append(openai_result)
            print("gpt35_res:{}".format(openai_result))
            time.sleep(3)

        elif args.bot_type == "glm130b":   # 请求glm130b
            req_130b_api = ReqGLM_130b()
            prompt = ori_prompt+content
            prompt = ori_prompt.format(ori_source,ori_content,ori_source)


            res_130b = req_130b_api.req_gpt(prompt)
            res_list.append(res_130b)
            print("glm130b_res:{}".format(res_130b))
            time.sleep(8)

        elif args.bot_type == "glm6b":  # 请求glm6b
            req_6b_api = ReqGLM_6b()
            prompt = ori_prompt+content
            prompt = ori_prompt.format(ori_source,ori_content,ori_source)


            res_6b = req_6b_api.req_6b(prompt)
            res_list.append(res_6b)
            print("sixb_res:{}".format(res_6b))
            time.sleep(3)

        elif args.bot_type == "minimax":     # 请求minimax
            req_minimax_api = Req_minimax()
            prompt = ori_prompt+content
            prompt = prompt.format(ori_source)
            input_list.append(prompt)
            res_minimax = req_minimax_api.req_minimax(prompt)
            res_list.append(res_minimax)
            
            print("prompt:{}".format(prompt))
            print("minimax_res:{}".format(res_minimax))
            # time.sleep(3)

            # break

            # print(json.dumps({"prompt": query_input, "res": res_list}, ensure_ascii=False))

    df1 = pd.DataFrame({'PROMPT': input_list, 'res': res_list})
    output_path = "res_"+args.task+"_"+args.bot_type+"_liuyi.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        df1.to_excel(writer, sheet_name=sheet_name, index=False)
    
        
        






