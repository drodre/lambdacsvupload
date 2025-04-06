import sys
import boto3
import json

def test_lambda_trigger(bucket_name, lambda_arn):
    s3 = boto3.client('s3')
    lambda_client = boto3.client('lambda')

    s3.put_object(
        Bucket=bucket_name,
        Key="test_auto.csv",
        Body="id,value\n1,100\n2,200\n3,300"
    )
    print("✅ File uploaded to S3")


    response = lambda_client.invoke(
        FunctionName=lambda_arn.split(":")[-1],
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "Records": [{
                "s3": {
                    "bucket": {"name": bucket_name},
                    "object": {"key": "test_auto.csv"}
                }
            }]
        })
    )
    print("🔹 Lambda response:", response['Payload'].read().decode())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_trigger.py <bucket_name> <lambda_arn>")
        sys.exit(1)
    
    test_lambda_trigger(sys.argv[1], sys.argv[2])