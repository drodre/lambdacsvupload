# Procesamiento de CSV en S3 con Lambda

## Architecture
1. **S3 Bucket**: Store CSV files Almacena with SSE-S3 cypher.
2. **Lambda Function**: It activates when a CSV is uploaded, then process the file.
3. **IAM Roles**: Minimal permissions for Lambda(S3 read and logs).
4. **Event Notification**: S3 configuration to notify Lambda.
5. **Tests**: A folder where store files to test infra.

![Diagrama](https://i.imgur.com/XYZ.png) *Ejemplo de diagrama*

## Despliegue
1. **Minimal requirements**:
   - Pulumi CLI
   - AWS CLI
   - Python 3.7+

2. **Steps**:
   ```bash
   curl -sSL https://get.pulumi.com | sh
   alias pulumi=~/.pulumi/bin/pulumi
   python3 -m venv env
   source env/bin/activate
   env/bin/pip install -r requirements.txt
   pulumi stack init dev
   pulumi config set aws:region eu-west-1
   pulumi up```