import json
import os
import boto3

TAG="Login Aamhi unique Partner"

def execuete(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            partner = json.loads(data)
            email = partner["email"]
            password = partner["password"]
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
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    print(table)
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='email= :email and password= :password',
            ExpressionAttributeValues={
                ':email': {'S': email},
                'password': {'S': password}
            }
        )
        print(response)
        return len(response['Items']) > 0
    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False

