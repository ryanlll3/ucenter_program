#!/usr/bin/python
# _*_ coding:utf-8 _*_

import json
import ssl
import urllib
import urllib.request
import urllib.parse
import yaml
from core.Logger import *

config_file = open('main_config/config.yml', 'r', encoding='utf-8')
config_variables = config_file.read()
conf = yaml.load(config_variables, Loader=yaml.FullLoader)

UCENTER_API_URL = conf.get('UCENTER_HOST').get('UCENTER_API_URL')
USER = conf.get('UCENTER_HOST').get('USER')
PASSWORD = conf.get('UCENTER_HOST').get('PASSWORD')


class UCenter:
    @setup_log
    def __init__(self, ucenter_url=UCENTER_API_URL, user=USER, password=PASSWORD):
        self.ucenter_url = ucenter_url
        self.user = user
        self.password = password

    def http(self, method, base_path, request_path, body=None, query_parameter=None):
        if method == 'GET':
            full_url = self.ucenter_url + base_path + request_path + "?" + query_parameter
            return self.http_get(full_url, self.token())
        elif method == 'POST':
            if query_parameter:
                full_url = self.ucenter_url + base_path + request_path + "?" + query_parameter
                return self.http_post(full_url, body, self.token())
            else:
                full_url = self.ucenter_url + base_path + request_path
                return self.http_post(full_url, body, self.token())

    def http_get(self, full_url, token):
        logging.info('Starting new HTTP Get request: %s' % full_url)
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        req = urllib.request.Request(full_url, headers=headers)
        if token:
            req.add_header('X-Auth-Token', token)
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(req, context=context)
        logging.info('HTTP Get Request Complete: %s' % full_url)
        return response.read()

    def http_delete(self, full_url, token):
        logging.info('Starting new HTTP Delete request: %s' % full_url)
        req = urllib.request.Request(full_url)
        if token:
            req.add_header('X-Auth-Token', token)
        req.add_header('Accept', 'application/json')
        req.get_method = lambda: 'DELETE'
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(req, context=context)
        logging.info('HTTP Delete Complete: %s' % full_url)
        return response.read()

    def http_post(self, full_url, jdata, token):
        logging.info('Starting new HTTP Post request: %s' % full_url)
        jdata = json.dumps(jdata).encode()
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        req = urllib.request.Request(full_url, jdata, headers)
        if token:
            req.add_header('X-Auth-Token', token)
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(req, context=context)
        logging.info('HTTP Post Complete: %s' % full_url)
        return response.read()

    def token(self):
        auth = {'userName': self.user, 'passWord': self.password}
        full_url = self.ucenter_url + '/token/generate'
        resp = self.http_post(full_url, auth, '')
        response_data = json.loads(resp)
        logging.info('Token Request Status:%s' % response_data['msg'])
        try:
            jsonData = json.loads(resp)
            token = jsonData['token']
        finally:
            logging.info('Token Request End: %s' % full_url)
        return token


if __name__ == '__main__':
    u_center = UCenter()
    token = u_center.token()
    print("X-Auth-Token:\n%s" % token)
