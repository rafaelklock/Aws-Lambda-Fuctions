import json
import urllib3
import os


url_http = 'http://ifconfig.me'

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    ipexterno = http.request('GET', url_http)
    return {'IP': ipexterno.data}
