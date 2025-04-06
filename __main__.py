import pulumi
import pulumi_aws as aws
import json

bucket = aws.s3.Bucket("csv-uploads",
    server_side_encryption_configuration={
        "rule": {
            "apply_server_side_encryption_by_default": {
                "sse_algorithm": "AES256"
            }
        }
    }
)

lambda_role = aws.iam.Role("lambdaRole",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }]
    })
)

s3_policy = aws.iam.RolePolicy("lambdaS3Policy",
    role=lambda_role.id,
    policy=bucket.arn.apply(lambda arn: json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": ["s3:GetObject"],
            "Effect": "Allow",
            "Resource": f"{arn}/*"
        }]
    }))
)

aws.iam.RolePolicyAttachment("lambdaBasicExecution",
    role=lambda_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
)


lambda_func = aws.lambda_.Function("csvProcessor",
    role=lambda_role.arn,
    runtime="python3.9",
    handler="handler.handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./lambda")
    }),
    timeout=60,
    environment={
        "variables": {"LOG_LEVEL": "INFO"}
    }
)

lambda_permission = aws.lambda_.Permission("s3InvokePermission",
    action="lambda:InvokeFunction",
    function=lambda_func.name,
    principal="s3.amazonaws.com",
    source_arn=bucket.arn
)

bucket_notification = aws.s3.BucketNotification("bucketNotification",
    bucket=bucket.id,
    lambda_functions=[aws.s3.BucketNotificationLambdaFunctionArgs(
        lambda_function_arn=lambda_func.arn,
        events=["s3:ObjectCreated:*"],
        filter_suffix=".csv"
    )]
)

pulumi.export("bucket_name", bucket.id)
pulumi.export("lambda_arn", lambda_func.arn)