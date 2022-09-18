import json
import urllib3
import time
import os
import uuid
import boto3

s3 = boto3.resource('s3')

DEP_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
BASE_DIR = "/tmp"

def lambda_handler(event, context):
    
    DEP_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
   
    manager = urllib3.PoolManager()
    r = manager.request('GET', DEP_URL)
    res = json.loads(r.data.decode('utf-8')) 
                
    dep_list = {}
    dep_list["departmentIds"] = []
    wanted_list = ["Greek and Roman Art", "Modern Art" , "Ancient Near Eastern Art", "Arms and Armor" , "The Robert Lehman Collection"]
                
    for i in res['departments']:
        if i["displayName"] in wanted_list:
            dep_list["departmentIds"].append({"departmentId": i["departmentId"]})
    
    return dep_list
