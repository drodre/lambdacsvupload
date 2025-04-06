import boto3
import os
import json
import uuid
import pytest

@pytest.fixture
def setup_resources():   
    return {
        "bucket_name": os.getenv('BUCKET_NAME'),
        "lambda_arn": os.getenv('LAMBDA_ARN')
    }

def test_lambda_trigger(aws_credentials, setup_resources):
    # Configura clientes AWS
    s3 = boto3.client('s3')
    lambda_client = boto3.client('lambda')

    bucket_name = setup_resources["bucket_name"]
    lambda_arn = setup_resources["lambda_arn"]

    if not bucket_name or not lambda_arn:
        pytest.skip("BUCKET_NAME oe LAMBDA_ARN variables missed")

    test_key = f"test_auto_{uuid.uuid4().hex[:6]}.csv"
    s3.put_object(
        Bucket=bucket_name,
        Key=test_key,
        Body="id,value\n1,100\n2,200\n3,300"
    )
    print(f"✅ File {test_key} uploaded to {bucket_name}")

    response = lambda_client.invoke(
        FunctionName=lambda_arn,
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "Records": [{
                "s3": {
                    "bucket": {"name": bucket_name},
                    "object": {"key": test_key}
                }
            }]
        })
    )
    
    result = json.loads(response['Payload'].read().decode())
    print("🔹 Lambda response:", result)
    assert result.get("status") == "OK"

    s3.delete_object(Bucket=bucket_name, Key=test_key)