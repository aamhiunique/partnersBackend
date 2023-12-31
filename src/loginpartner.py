import json
import os


TAG="Login Aamhi unique Partner"

def execute(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            partner = json.loads(data)
            email = partner["partnerEmail"]
            password = partner["partnerPassword"]
            partnerExists = get_partner_by_email_password(email, password)
            if partnerExists:
                return {
                        "statusCode": "200",
                        "body": f'Welcome partner {email}'
                        }
            else:
                return {
                        "statusCode": "206",
                        "body": f'Partner not registered with email {email} '
                        }
    except Exception as ex:
            print("Error in Login partner")
            return {
                    "statusCode": "503",
                    "body": "Error while login"
            }

def get_partner_by_email_password(email, password):
    dynamodb = boto3.client('dynamodb')
    table = os.environ.get("AAMHI_UNIQUE_PARTNER_REGISTER_TABLE")
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='partnerEmail= :partnerEmail and partnerPassword= :partnerPassword',
            ExpressionAttributeValues={
                ':partnerEmail': {'S': email},
                ':partnerPassword': {'S': password}
            }
        )
        return len(response['Items']) > 0
    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False

