import boto3
import os
import uuid

def upload_csv_to_s3():   
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = os.getenv('AWS_REGION', 'eu-west-1')
    bucket_name = os.getenv('BUCKET_NAME')

    if not all([aws_access_key_id, aws_secret_access_key, bucket_name]):
        print("Error: enviroment variables missed (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME)")
        return
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    
    file_name = f"manual_test_{uuid.uuid4().hex[:6]}.csv"
    csv_content = "id,value\n1,100\n2,200\n3,300"

    try:        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=csv_content
        )
        print(f"✅ File {file_name} successfully uploaded to {bucket_name}")
                
        return {
            "status": "OK",
            "bucket": bucket_name,
            "file_name": file_name
        }
    except Exception as e:
        print(f"❌ Error when uploading file: {str(e)}")
        return {
            "status": "ERROR",
            "error": str(e)
        }

if __name__ == "__main__":
    upload_csv_to_s3()