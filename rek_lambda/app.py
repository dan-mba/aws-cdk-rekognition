import json
import base64
import boto3
from botocore.exceptions import ClientError

client = boto3.client('rekognition')


def fix_label(label):
    return {
        "Name": label['Name'],
        "Confidence": label['Confidence']
    }


def handler(event, context):
    if 'body' not in event:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "no body",
            }),
        }

    try:
        body = event['body']
        img_decoded = base64.b64decode(body)

        rek = client.detect_labels(
            Image={
                'Bytes': img_decoded
            }
        )

    except ClientError as error:
        return {
            "statusCode": "200",
            "body": json.dumps(error.response['Error'])
        }
    except Exception as error:
        return {
            "statusCode": "200",
            "body": json.dumps({
                "message": str(error)
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(list(map(fix_label, rek['Labels']))),
    }
