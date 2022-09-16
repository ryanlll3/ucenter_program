#!/usr/bin/python
# _*_ coding:utf-8 _*_

from core.UCenter import *
from core.UCenterDB import *

# 根据需要调整查询条件

query = {
    "isAbstract": '',
    "isUserdefined": '',
    "noField": True,
}


body = {}

# 查询条件结束

config_file = open('cmdb/cmdb_config.yml', 'r', encoding='utf-8')
config_variables = config_file.read()
conf = yaml.load(config_variables, Loader=yaml.FullLoader)

http_method = conf.get('CI_Types').get('HTTP_METHOD')
base_path = conf.get('CI_Types').get('BASE_PATH')
request_path = conf.get('CI_Types').get('REQUEST_PATH')
table = conf.get('CI_Types').get('TABLE')
column1 = conf.get('CI_Types').get('COLUMN1')
column2 = conf.get('CI_Types').get('COLUMN2')
column3 = conf.get('CI_Types').get('COLUMN3')
columns = (column1, column2, column3)
query_parameter = urllib.parse.urlencode(query)

rows = []


def get_data(url, token):
    logging.info("Loading: %s" % url)
    try:
        resp = u_center.http_get(url, token)
        result = json.loads(resp)
        for item in result:
            row = [item["typeCode"], item["name"], current_time]
            rows.append(row)
            # result_json_format = json.dumps(result, indent=4)
            # print(result_json_format)
    except Exception as e:
        logging.exception(e)
    return rows


def post_data(url, body, token):
    logging.info("Loading: %s" % url)
    try:
        resp = u_center.http_post(url, body, token)
        result = json.loads(resp)
        for item in result:
            row = [item["typeCode"], item["name"], current_time]
            rows.append(row)
            # result_json_format = json.dumps(result, indent=4)
            # print(result_json_format)
    except Exception as e:
        logging.exception(e)
    return rows


if __name__ == '__main__':
    u_center = UCenter()
    u_center_db = UCenterDB()
    if http_method == 'GET':
        full_url = UCENTER_API_URL + base_path + request_path + "?" + query_parameter
        get_data(full_url, u_center.token())
    elif http_method == 'POST':
        full_url = UCENTER_API_URL + base_path + request_path
        post_data(full_url, body, u_center.token())

    try:
        u_center_db.clear_table(table)
        u_center_db.insert_into_table(table, columns, rows)
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info('Exiting')


