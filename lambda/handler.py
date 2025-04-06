import boto3
import csv
import json

def handler(event, context):
    print("Event received:", json.dumps(event))
    
    if 'Records' not in event:
        print("Error: Event has no Records")
        return {"status": "ERROR", "message": "Wrong vent format"}
    
    s3 = boto3.client('s3')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"Processing{key} in {bucket}")
                
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read().decode('utf-8')
        
        reader = csv.reader(data.splitlines())
        rows = list(reader)
        char_count = len(data)  
        
        print(f"File {key} has {len(rows)} rows and {char_count} characters")
        
        return {
            "status": "OK",
            "rows": len(rows),
            "characters": char_count
        }