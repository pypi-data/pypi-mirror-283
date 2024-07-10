"""
Created on 06 09 21:35:20 2024

@project: damip
@author : kaiwei.li
@company: Digitopia Robotics Ltd.,Co.
"""

import re
import aioredis
import asyncio
from zhipuai import ZhipuAI

import logging

from damip_robots import config

from aioredis.exceptions import ConnectionError

# Set logging level
logging.basicConfig(level=logging.INFO, format=':) %(asctime)s %(levelname)s: %(message)s')

# get glm key and prompt from redis
async def init():
    try:
        redis = aioredis.from_url(config.REDIS_SERVER)
        
        value = await redis.get('PARAM:ZHIPU:KEY')
        REDIS_ZHIPU_KEY = value
        
        value = await redis.get('PARAM:ZHIPU:PROMPT')
        REDIS_ZHIPU_PROMPT = value.decode('utf-8')
        
        return REDIS_ZHIPU_KEY, REDIS_ZHIPU_PROMPT 

    except ConnectionError as e:
        REDIS_ZHIPU_KEY = ""
        REDIS_ZHIPU_PROMPT = ""
        logging.info(':) Could not connect to Redis: ' + {e})
    finally:
        await redis.close()

# find functions in answer
def extract(answer):
    functions_args = []
    functions_name = []
    """
    提取字符串中所有DIGITOPIA.后面的函数名和括号内的参数。

    参数:
    s (str): 包含函数调用的字符串。

    返回:
    list: 包含所有匹配项的列表，每个匹配项是一个元组(函数名, 参数)。
    """
    # 使用正则表达式匹配所有函数调用
    matches = re.findall(r'DIGITOPIA\.(.*?)\((.*?)\)', answer)

    for function_name, function_args in matches:
        # logging.info("函数:" + function_name)
        # logging.info("参数:" + function_args)
        functions_name.append(function_name)
        functions_args.append(function_args)
    
    return functions_name, functions_args

# transfer functions to index
def transfer(functions_name, functions_args):
    functions_index = []
    for function_name, function_args in zip(functions_name, functions_args):
        logging.info("function_name:" + function_name)
        logging.info("function_args:" + function_args)

        if "head_shake" in function_name:
            functions_index.append(1)
        elif "left_arm_shake" in function_name:
            functions_index.append(2)
        elif "right_arm_shake" in function_name:
            functions_index.append(3)
        elif "wheels_move" in function_name:
            functions_index.append(4)
        elif "voice_play" in function_name:
            functions_index.append(9)
        else:
            functions_index.append(0)
    return functions_index

# glm cloud
def request(ask):

    messages=[
    {"role": "user", "content": prompt},
    {"role": "user", "content": ask}
    ]

    response = client.chat.completions.create(
    model="glm-4", # 填写需要调用的模型名称
    messages=messages,
    #stream=True,
    #top_p=0.7,
    #temperature=0.95,
    #max_tokens=1024,
    #stream=True,
    )
   
    # for trunk in response:
    #     print(trunk)
    
    res = response.choices[0].message

    answer = str(res.content)

    return answer



REDIS_ZHIPU_KEY, REDIS_ZHIPU_PROMPT = asyncio.run(init())

key = REDIS_ZHIPU_KEY
prompt = REDIS_ZHIPU_PROMPT
client = ZhipuAI(api_key=key.decode('utf-8'))



# USER_ASK = "你听到有人问你<机器人摇摇头>，你应该怎么回应？如果你需要执行动作，请给出执行命令；如果你需要回答对方的提问，你可以将答案通过声卡播放。"

# # 1. get answer from glm cloud server
# answer = request(USER_ASK)
# logging.info(':) Glm Cloud Answer:' + str(answer))

# # 2. find functions in string
# functions_name, functions_args = extract(answer)
# logging.info(':) Glm Cloud Function:' + str(functions_name) + str(functions_args))

# # 3. execute functions
# functions_index = transfer(functions_name, functions_args)
# logging.info(':) Glm Cloud Function Index:' + str(functions_index))

# # 4. return answer and functions index
# print(answer, functions_index)


# test_str = "DIGITOPIA.voice_play('我的型号是射线巡游机，是由“数码大陆”公司设计制造。')"
# functions_name, functions_args = extract(test_str)
# logging.info(':) Glm Cloud Function:' + str(functions_name) + str(functions_args))

