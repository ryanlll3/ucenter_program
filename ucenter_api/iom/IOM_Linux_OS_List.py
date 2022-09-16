#!/usr/bin/python
# _*_ coding:utf-8 _*_

from core.UCenter import *
from core.UCenterDB import *

# 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~

query = {}

body = {
    'appType': 'linux',
    'size': '-1',
    'start': '-1'
}

config_file_yaml = 'iom/iom_config.yml'
API = 'IOM_Linux_OS_List'
table_columns_count = 8

# 查询条件结束 ~ 查询条件结束 ~ 查询条件结束 ~ 查询条件结束 ~ 查询条件结束 ~ 查询条件结束 ~ 查询条件结束 ~ 查询条件结束 ~ 查询条件结束 ~

config_file = open(config_file_yaml, 'r', encoding='utf-8')
config_variables = config_file.read()
conf = yaml.load(config_variables, Loader=yaml.FullLoader)

http_method = conf.get(API).get('HTTP_METHOD')
base_path = conf.get(API).get('BASE_PATH')
request_path = conf.get(API).get('REQUEST_PATH')
table = conf.get(API).get('TABLE')
query_parameter = urllib.parse.urlencode(query)


def analyze_data(result):
    # 若是重新分析数据，可以解除下两行注释，复制到JSON文件中，以便分析，更新下面取参逻辑
    # result_json_format = json.dumps(result, indent=4)
    # print(result_json_format)
    rows = []
    for i in result["data"]["data"]:
        monitor_id = i["id"]
        name = i["name"]
        ip = i["ip"]
        appType = i["appType"]
        oneCategoryStr = i["oneCategoryStr"]
        format_data = deep_analyze_data(i)
        row = [monitor_id, name, ip, appType, oneCategoryStr] + format_data + [current_time]
        rows.append(row)
    return rows


def deep_analyze_data(_list):
    health = []
    if _list["health"] == -1:
        health.append("不限")
    elif _list["health"] == 0:
        health.append("正常")
    elif _list["health"] == 1:
        health.append("未知")
    elif _list["health"] == 3:
        health.append("通知")
    elif _list["health"] == 4:
        health.append("警告")
    elif _list["health"] == 5:
        health.append("次要")
    elif _list["health"] == 6:
        health.append("重要")
    elif _list["health"] == 7:
        health.append("紧急")
    else:
        health.append("")
    avail = []
    if _list["available"] == -1:
        avail.append("不限")
    elif _list["available"] == 0:
        avail.append("可用")
    elif _list["available"] == 2:
        avail.append("Ping不可达")
    elif _list["available"] == 3:
        avail.append("协议连接失败")
    elif _list["available"] == 4:
        avail.append("未监控")
    else:
        avail.append("")
    return avail + health


def get_data():
    try:
        u_center = UCenter()
        resp = u_center.http(http_method, base_path, request_path, body, query_parameter)
        logging.info("Loading %s%s%s" % (UCENTER_API_URL, base_path, request_path))
        result = json.loads(resp)
        return analyze_data(result)
    except Exception as e:
        logging.exception(e)


def get_columns(count):
    starting = 1
    columns = []
    while count > 0:
        columns = columns + [(conf.get(API).get('COLUMN' + str(starting)))]
        count = count - 1
        starting += 1
    return tuple(columns)


if __name__ == '__main__':
    u_center_db = UCenterDB()
    rows = get_data()
    try:
        u_center_db.clear_table(table)
        u_center_db.insert_into_table(table, get_columns(table_columns_count), rows)
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info('Exiting')

