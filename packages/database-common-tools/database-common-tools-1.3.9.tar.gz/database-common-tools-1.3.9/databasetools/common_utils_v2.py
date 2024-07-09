import hashlib
import requests
import bson.json_util
import json
from datetime import datetime

class CommonUtils:

    def __init__(self, log):
        self.log = log

    def dump_load(self, fn):
        with open(fn, 'r') as f:
            try:
                jmap = json.loads(f.read())
                return dict(jmap)
            except Exception as e:
                self.log.error('exception ... {}\tfile={}'.format(e, fn))
                return dict()
    
    def dump_loads(self, value):
        try:
            return bson.json_util.loads(value)
        except Exception as e:
            self.log.error('exception ... {}\tvalue={}'.format(e, value))
            return dict()
        
    def unix_to_formatted_time(self, unix_timestamp):
        """
        将Unix时间戳转换为格式化的时间字符串
        :param unix_timestamp: Unix时间戳(以秒为单位)
        :return: 格式化的时间字符串，格式为'%Y-%m-%d %H:%M:%S'
        """
        dt_object = datetime.fromtimestamp(unix_timestamp)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time
    
    def get_unix_time(self, time_str):
        """
        将格式化的时间字符串转换为Unix时间戳
        :param time_str: 格式化的时间字符串，格式为'%Y-%m-%d %H:%M:%S'
        :return: Unix时间戳(以秒为单位)
        """
        if time_str:
            try:
                dt_obj = datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
                unix_timestamp = int(dt_obj.timestamp())
                return unix_timestamp
            except ValueError as e:
                try:
                    dt_obj = datetime.strptime(str(time_str), "%Y-%m-%d")
                    unix_timestamp = int(dt_obj.timestamp())
                    return unix_timestamp
                except ValueError as e:
                    return 0
        else:
            return 0
    
    def image_exists_get(self, url, timeout=10, max_retries=3):
        """
        Check if an image exists at the given URL.
        
        :param url: Image URL
        :param timeout: Timeout for the request in seconds
        :param max_retries: Maximum number of retries
        :return: True if image exists, False otherwise
        """
        attempt = 0
        while attempt < max_retries:
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.RequestException as e:
                self.log.error('Check image exist error: '.format(e))
            attempt += 1
        return False

    def image_exists_head(self, url, timeout=10, max_retries=3):
        """
        Check if an image exists at the given URL.
        
        :param url: Image URL
        :param timeout: Timeout for the request in seconds
        :param max_retries: Maximum number of retries
        :return: True if image exists, False otherwise
        """
        attempt = 0
        while attempt < max_retries:
            try:
                response = requests.head(url, timeout=timeout)
                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.RequestException as e:
                self.log.error('Check image exist error: '.format(e))
            attempt += 1
        return False

    def parse_sql_result(self, cursor):
        """
        Parse SQL result from a cursor object and return as list of dictionaries.
        
        :param cursor: SQL cursor object
        :return: List of dictionaries with column names as keys
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def calculate_md5(self, input):
        """
        计算输入字符串的MD5哈希值, 并返回32位的十六进制字符串
        :param input_string: 输入字符串
        :return: 32位的MD5十六进制字符串
        """
        if isinstance(input, str):
            # 创建MD5哈希对象
            md5 = hashlib.md5()
            # 更新哈希对象的输入内容
            md5.update(input.encode())
            # 获取十六进制表示的MD5哈希值，并去除特殊符号
            md5_hex = md5.hexdigest()
            # 去除MD5字符串中的特殊符号
            md5_cleaned = ''.join(c for c in md5_hex if c.isalnum())
            # 返回32位的MD5十六进制字符串（无特殊符号）
            return md5_cleaned[:32]
        else:
            self.log.error('input not str,please input type str!')