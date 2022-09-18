import json
import urllib3
import time
import logging
import os
import uuid
import boto3

DEP_URL = "https://collectionapi.metmuseum.org/public/collection/v1/departments"

#OBJ_URL to get all unique IDs for all objects
OBJ_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

def lambda_handler(event, context):
    manager = urllib3.PoolManager()
    r = manager.request('GET', DEP_URL)
    department = json.loads(r.data.decode('utf-8')) 
    
    print("department is dictionary with only one key named departments and value is list of dictionaries")
    
    dep_list=[]
    
    for i in department:
        print(i)
        for j in department.get(i):
            print(j)
            dep_list.append(j)
    
    print("Each dictionary has 2 keys (departmentId,displayName)")  
    
    s = manager.request('GET', OBJ_URL)
    objects = json.loads(s.data.decode('utf-8')) 
    
    
    #getting all unique ids
    objectIDs = objects.get("objectIDs")
    object_list=[]
    
    #accessing each object by its unique id and storing it into list
    for i in objectIDs:
        object_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"+str(i)
        t = manager.request('GET', object_url)
        object = json.loads(t.data.decode('utf-8')) 
        object_list.append(object)
    
    print(object_list)

   
    return {
        'statusCode': 200,
        'department': json.dumps(dep_list),
        'objects' : json.dumps(object_list)
    }





