import json
import time
import os
import boto3
import urllib3

s3_client = boto3.client('s3')

S3_BUCKET = "damn-buckettask2"
BASE_DIR = "/tmp"

def get_object_ids(departmentID):

    OBJ_FOR_DEP = "https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds=" + str(departmentID)

    manager = urllib3.PoolManager()
    res = manager.request('GET', OBJ_FOR_DEP)
    objectIDs_in_dep = json.loads(res.data.decode('utf-8'))
    objekti = objectIDs_in_dep["objectIDs"]

    return objekti
                

def get_object(objectID):
    
    http = urllib3.PoolManager()
    API_URL = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(objectID)
    res = http.request("GET", API_URL)
    dict1 = json.loads(res.data.decode('utf-8'))
    
    constituents = dict1["constituents"]
    measurment = dict1["measurements"]
    
    
    if(constituents != None):
        for i in constituents:
            dict1["constituentID"]=i["constituentID"]
            dict1["constituent_role"] = i["role"]
            dict1["constituent_name"] = i["name"]
            dict1["constituent_constituentULAN_URL"]=i["constituentULAN_URL"]
    else:
        dict1["constituentID"]=None
        dict1["constituent_role"] = ""
        dict1["constituent_name"] = ""
        dict1["constituent_constituentULAN_URL"]= ""
    
    dict1["Depth"] = None
    dict1["Height"] =  None
    dict1["Width"] = None
    dict1["Lenght"]= None
    dict1["measurment_elementName"] =""
    dict1["measurment_elementDescription"] = ""
    
    if(measurment != None):
        for i in measurment:
            dict1["measurment_elementName"] = i["elementName"]
            dict1["measurment_elementDescription"] = i["elementDescription"]
            elementMeasurements=i["elementMeasurements"]
            
        for j in elementMeasurements:
            dict1[j] = elementMeasurements.get(j)
            
    
    dict1.pop("constituents")
    dict1.pop("measurements")
    
    return dict1

def get_and_write_objects(objectIDs):
    
    for objectID in objectIDs:
        objekt = get_object(objectID)

        object_department = objekt['department']
        objectID = objekt['objectID']
        
        object_department = object_department.replace(' ', '')
        
        JSON_NAME = os.path.join(BASE_DIR, str(objectID) + ".json")
        with open(JSON_NAME, 'w') as f:
            json.dump(objekt, f)
        s3_client.upload_file(JSON_NAME , S3_BUCKET, "department=" + object_department + "/" + str(objectID) + ".json")
    
    
def lambda_handler(event, context):
    departmentID = event['departmentId']
    
    
    objectIDs = get_object_ids(departmentID)
    
    get_and_write_objects(objectIDs)
        
    return 0