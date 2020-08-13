import json
import boto3
from botocore.client import Config
import urllib3



def lambda_handler(event, context):

    url_http = 'http://ifconfig.me'
    http = urllib3.PoolManager()
    ipexterno = http.request('GET', url_http)
    print(f"{ipexterno.data}")
    
    
    config = Config(connect_timeout=3, retries={'max_attempts': 0})
    
    s3 = boto3.resource('s3', config=config)
    
    my_bucket = s3.Bucket('amplify-testpushreact-dev-111659-deployment')
    
    for my_bucket_object in my_bucket.objects.all():
        print(my_bucket_object)
        


    
    return {
        'statusCode': 200
    }
