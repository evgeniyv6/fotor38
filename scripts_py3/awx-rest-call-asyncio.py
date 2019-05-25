#!/usr/bin/env python
# min - py 3.4

import os, sys
import json
import configparser
import itertools
from collections import namedtuple
from concurrent.futures import FIRST_COMPLETED
import asyncio
import requests
sys.path.insert(0,'/tmp/sec')
import cryppass

CONFIG = configparser.ConfigParser()
CONFIG_FILE = os.path.dirname(__file__)+'/params.ini'
CERT = os.path.dirname(__file__)+'/sslcert.cer'
TAGS = namedtuple('TAGS','job tags awxu awxh awxurl pl awxjob')
SLEEP_SECONDS = 1

'''
For POSTMAN
Launch some JOB:
https://someawxhost.ru/api/v2/job_templates/1/launch/
raw:
{"id": 1,
 "type": "job_template",
  "url": "/api/v2/job_templates/1/",
  "related": {
	"launch": "/api/v2/job_templates/1/launch/"
	},
 "job_tags": "test"
}

Get some JOB state:
https://someawxhost.ru/api/v2/jobs/2/
raw:
{"results":
        {
            "type": "job_event",
            "related": {
                "job": "/api/v2/jobs/2/"
            },
            "summary_fields": {
                "job": {
                    "id": 2
                       }
            }
         
        }
}
'''

def call_awx(awx_uri, req, headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'},getval=False):
    try:
        if getval is True:
            res = requests.get(awx_uri,data=json.dumps(req), headers=headers, verify=CERT)
        else:
            res = requests.post(awx_uri,data=json.dumps(req), headers=headers, verify=CERT)
    except requests.exceptions.HTTPError as errhttp:
        print('\t##### HTTP ERROR #####\n',errhttp)
        print('\t##### EXIT #####')
        sys.exit(1)
    except requests.exceptions.ConnectionError as errconn:
        print('\t##### CONNECTION ERROR #####\n', errconn)
        print('\t##### EXIT #####')
        sys.exit(1)
    except requests.exceptions.ReadTimeout as errread:
        print('\t##### READ ERROR #####\n', errread)
        print('\t##### EXIT #####')
        sys.exit(1)
    else:
        jsonresp = json.loads(res.content)
        try:
            print('\t##### PERMISSION ERROR ######\n',jsonresp['detail'])
            sys.exit(1)
        except KeyError:
            return jsonresp

def getconfig(conf_file, env):
    try:
        CONFIG.read(conf_file)
    except IOError as err:
        print("\t##### Error while reading config file: #####\n", err)
        print('\t##### EXIT #####')
        sys.exit(1)
    try:
        tags = CONFIG.get('GLOBAL', "tags")
        awxuser = CONFIG.get('GLOBAL', 'basicauthuser')
        awxpwd = CONFIG.get('GLOBAL', 'basicauthhash')
        awxuri = CONFIG.get('GLOBAL', "awxurl")
        awxjob = CONFIG.get('GLOBAL', "awxjobstate")
        pl = CONFIG.get('GLOBAL', "password_length")
        job = CONFIG.get(env, "job_number")
    except IOError as err:
        print("\t##### Error reading parameters from file: #####\n", err)
        sys.exit(1)
    return TAGS(job,tags,awxuser,awxpwd,awxuri,pl,awxjob)

def startawxjob(env, item):
    global data, headers
    data = getconfig(CONFIG_FILE, env)
    if item == 'TEST': jvar = data.job
    else: pass # for another items
    awxurl = data.awxurl + jvar + "/launch/"
    if int(jvar) > 0:
        req = {"id": jvar, "type": "job_template", "url": "/api/v2/job_templates/"+ jvar +"/","related": {"launch": "/api/2/job_templates/"+ jvar +"/launch/"}, "job_tags": data.tags}
    else:
        print('\t###### NO SUCH JOB ######\n')
        sys.exit(1)
    headers = {'Authorization': 'Basic '+cryppass.enc_dec_func(2,data.awxh,int(data.pl)),'Content-Type': 'application/json', 'cache-control': 'no-cache'}
    res = call_awx(awxurl, req, headers)
    try:
        jobnum = res['job']
    except KeyError as errk:
        print("\t##### AWX DIDN'T RETURN JOB NUMBER ######\n")
        sys.exit(1)
    else:
        print('\t###### AWX JOB NUMBER {} ######'.format(jobnum))
        return jobnum

@asyncio.coroutine
def getjobstate(jobnum):
    jobnum=str(jobnum)
    awxjobstate = data.awxjob + jobnum
    reqjob = {"results":{"type": "job_event","related": {"job": "/api/v2/jobs/"+jobnum+"/"},"summary_fields": {"job": {"id": jobnum}}}}
    jobstate = call_awx(awxjobstate,reqjob,headers,getval=True)
    try:
        if jobstate['status'] == 'successful':
            print('\t###### JOB SUCCESSFULLY COMPLETED ######')
            return True
        elif jobstate['status'] == 'failed':
            print('\t\n###### JOB FAILED ######')
            sys.exit(1)
        else:
            return False
    except KeyError as errk:
        print("\t##### AWX DIDN'T RETURN STATUS STATE ######\n")
        sys.exit(1)

@asyncio.coroutine
def spinner():
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        write(char)
        flush()
        write('\x08'*len(char))
        try:
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            break

@asyncio.coroutine
def jobone(jobnum):
    res = yield from getjobstate(jobnum)
    while not res:
        print('# JOB STILL RUNNING. SLEEP UNTIL NEXT STATE CALL FOR {:.1f} SEC'.format(SLEEP_SECONDS))
        yield from asyncio.sleep(SLEEP_SECONDS)
        res = yield from getjobstate(jobnum)

@asyncio.coroutine
def run(jobnum):
    primer = asyncio.ensure_future(jobone(jobnum))
    spin = asyncio.ensure_future(spinner())
    done, pending = yield from asyncio.wait([primer, spin], return_when=FIRST_COMPLETED)
    for future in pending: future.cancel()

def main():
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " env param2")
        sys.exit(0)
    env=sys.argv[1]
    jobn=startawxjob(env,sys.argv[2])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(jobn))
    loop.close()

if __name__=='__main__':
    main()




