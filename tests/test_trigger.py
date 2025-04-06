import boto3
import os
import json
import pytest

# Configuración desde variables de entorno (se configuran en GitHub Actions)
@pytest.fixture
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
    os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
    os.environ['AWS_REGION'] = os.getenv('AWS_REGION', 'us-east-1')

@pytest.fixture
def setup_resources():
    # Estos valores deben ser inyectados desde los outputs de Pulumi
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
        pytest.skip("Faltan variables de entorno BUCKET_NAME o LAMBDA_ARN")

    # 1. Sube archivo de prueba
    test_key = "test_auto.csv"
    s3.put_object(
        Bucket=bucket_name,
        Key=test_key,
        Body="id,value\n1,100\n2,200"
    )
    print(f"✅ Archivo {test_key} subido a {bucket_name}")

    # 2. Invoca Lambda
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
    print("🔹 Respuesta Lambda:", result)
    assert result.get("status") == "OK"

    # 3. Limpieza
    s3.delete_object(Bucket=bucket_name, Key=test_key)