#!/usr/bin/python
# _*_ coding:utf-8 _*_

from core.UCenter import *
from core.UCenterDB import *

# 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~ 根据需要调整查询条件 ~

query = {
    "ciTypeCode": "",
    "total": True
}

body = {}

config_file_yaml = 'cmdb/cmdb_config.yml'
API = 'CI_Lists'
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
    for i in result["rsCis"]:
        cid = i["id"]
        name = i["name"]
        type_code = i["typeCode"]
        type_name = i["typeName"]
        ci_field_list = i["itemList"]
        format_data = deep_analyze_data(ci_field_list)
        row = [cid, name, format_data[0], type_code, type_name, format_data[1], format_data[2]] + [current_time]
        rows.append(row)
    return rows


def deep_analyze_data(_list):
    # 内循环解析
    l1 = []
    for field_dict in _list:
        if field_dict["key"] == "ip_address":
            l1.append(field_dict["value"])
    if not l1:
        l1.append("")
    # 内循环解析
    l2 = []
    for field_dict in _list:
        if field_dict["key"] == "physical_location":
            l2.append(field_dict["value"])
    if not l2:
        l2.append("")
    # 内循环解析
    l3 = []
    for field_dict in _list:
        if field_dict["key"] == "monitor_id":
            l3.append(field_dict["value"])
    if not l3:
        l3.append("")
    # 得出以上所有内循环解析的列表
    return l1 + l2 + l3


def get_data(method, base_path, request_path, body, query_parameter):
    try:
        resp = u_center.http(method, base_path, request_path, body, query_parameter)
        logging.info("Loading %s%s%s" % (UCENTER_API_URL, base_path, request_path))
        result = json.loads(resp)
        return analyze_data(result)
    except Exception as e:
        logging.exception(e)
        return


def get_columns(count):
    starting = 1
    columns = []
    while count > 0:
        columns = columns + [(conf.get(API).get('COLUMN' + str(starting)))]
        count = count - 1
        starting += 1
    return tuple(columns)


if __name__ == '__main__':
    u_center = UCenter()
    u_center_db = UCenterDB()
    rows = get_data(http_method, base_path, request_path, body=body, query_parameter=query_parameter)
    try:
        u_center_db.clear_table(table)
        u_center_db.insert_into_table(table, get_columns(table_columns_count), rows)
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info('Exiting')

