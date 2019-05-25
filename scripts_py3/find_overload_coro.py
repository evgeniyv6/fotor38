#!/usr/bin/env python

# py 3.7 recommended, minimal -3.4

import os, sys
import smtplib
import datetime
import requests
import json
import configparser
from collections import namedtuple, defaultdict
from functools import wraps

CONFIG = configparser.ConfigParser()
CONFIG_FILE = os.path.dirname(__file__)+'/some.conf'
RESULT = namedtuple('RESULT','min max average')
MAX_SIZE_SEARCH = 500

def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen=func(*args, **kwargs)
        next(gen)
        return gen
        return primer


def select_server(hosts=None):
    if hosts is None:
        sys.exit(1)
    else:
        def_hosts = list(hosts)
        for host in def_hosts:
            working_host = True if os.system('ping -c 1 ' + host + '>/dev/null 2>&1') is 0 else False
            if working_host is True: break
            if host == def_hosts[-1]:
                sys.exit(1)
    return host

def create_elastic_link(elastic_host, elastic_port, elastic_index, uri_tail):
    rotation = '{}.{:02d}'.format(datetime.datetime.now().year, datetime.datetime.now().month)
    url = 'http://'+elastic_host+':'+elastic_port+'/'+elastic_index+str(rotation)+'/'+uri_tail
    return url

def timestamps_files_for_zabbix(env):
    script_path = os.path.dirname(__file__)
    delta = datetime.timedelta(hours=3)
    ...

def apic_request(elastic_uri, req, headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}):
    res = requests.post(elastic_uri,data=json.dumps(req), headers=headers)
    return json.loads(res.content)

def indicators_subgen():
    count, summ = 0, 0.0
    min, max = 1000,0
    avg = None
    while 1:
        item = yield
        if item is None: break
        min=item if item<min else min
        max=item if item>max else max
        summ += item
        count +=1
        avg = summ/count
    return RESULT(min,max,avg)

#@coroutine
def grouper_deleggen(res,key):
    while 1:
        res[key] = yield from indicators_subgen()

def collect_data(json_format):
    ...
    # return list of dictionary: key: name and version, value: list of indicators


def main():
    if len(sys.argv) < 2 :
        print("Usage: "+sys.argv[0]+" env")
        sys.exit(0)
    try:
        CONFIG.read(CONFIG_FILE)
    except IOError as err:
        print("Error while reading config file: "), err
    try:
        env = sys.argv[1]
        threshold = CONFIG.get(env, "threshold")
        ehosts = CONFIG.get(env, "elastic_hosts")
        ehost = select_server([host for host in ehosts.split('|')])
        eport = CONFIG.get(env, "elastic_port")
        eindex = CONFIG.get(env, "elastic_index")
        euri = CONFIG.get(env, "uri_tail")
        elastic_url = create_elastic_link(ehost, eport, eindex, euri)
    except IOError as err:
        print("Error reading parameters from file: "), err
        sys.exit(1)

    time_from, time_to = timestamps_files_for_zabbix(env)
    req = {...}
    json_req = apic_request(elastic_url, req)
    res={}
    if <thresh param> > 0:
        data_dict = collect_data(json_req)
        for point in data_dict.items():
            group = grouper_deleggen(res,point[0])
            next(group)
            for i in point[1]:
                group.send(i)
            group.send(None)
        reporter(res)
    else:
        print("OK")

def reporter(data):
    for k,v in sorted(data.items()):
        a,b,c = k.split(';')
        msg = 'A: {}. B: {}. C: {}. Overload: min - {}, max - {}, average - {:.2f}'.format(a, b, c, v.min, v.max, float(v.average))
        print(msg)

if __name__=='__main__':
    main()