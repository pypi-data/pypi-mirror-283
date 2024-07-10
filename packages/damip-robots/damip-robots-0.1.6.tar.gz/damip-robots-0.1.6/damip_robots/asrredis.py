"""
Created on 06 28 01:35:20 2024

@project: damip
@author : kaiwei.li
@company: Digitopia Robotics Ltd.,Co.
"""

import os
import aioredis
from datetime import datetime
import time

import logging

from damip_robots import config

from aioredis.exceptions import ConnectionError

# Set logging level
logging.basicConfig(level=logging.INFO, format=':) %(asctime)s %(levelname)s: %(message)s')

TIME_THRESHOLD = 5 # only handle asr result in 5 seconds
timestamp_record = ""

def calculate_time_difference(timestamp1, timestamp2):
    format_str = '%Y-%m-%d %H:%M:%S'
    try:
        # 将字符串转换为 datetime 对象
        time1 = datetime.strptime(timestamp1, format_str)
        time2 = datetime.strptime(timestamp2, format_str)

        # 计算时间间隔
        time_difference = time2 - time1

        # 将时间间隔转换为秒数
        seconds_difference = time_difference.total_seconds()

        # 输出时间间隔（以秒为单位）
        print(f'Time difference in seconds: {seconds_difference}')
        return seconds_difference
    except ValueError as e:
        print(f"Error: {e}. Please provide timestamps in the format 'YYYY-MM-DD HH:MM:SS'.")


async def sync():
    try:
        global timestamp_record
        
        # select db id
        robot = str(config.ROBOT_IDMARK)
        print(":) Robot name:" + robot)
        redis_dbid = int(robot[-3:]) # get the last 3 number
        await redis.execute_command('SELECT', redis_dbid)
        logging.info(':) Redis DB SELECT:' + str(redis_dbid))
        
        # get the last TRANS
        value = await redis.lindex('TRANS:'+robot[-8:], -1)
        value = value.decode('utf-8')
        timestamp1 = value[0:19]
        
        if str(timestamp_record) == str(timestamp1):
            return False, 0, 0
        else:
            timestamp_record = timestamp1
        
        timestamp2 = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) 
        time_diff = calculate_time_difference(timestamp1, timestamp2)

        if time_diff <= TIME_THRESHOLD:
            return True, time_diff, value[20:]
        else:
            return False, 0, 0

    except ConnectionError as e:
        await redis.close()
        print(f"Could not connect to Redis: {e}")
    # finally:
    #     await redis.close()

# FLAG, TIME_DIFF, ASR_RESULT = asyncio.run(sync())

redis = aioredis.from_url(config.REDIS_SERVER)
