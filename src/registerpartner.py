import json
import os
import boto3
import uuid

TAG="Register Aamhi unique Partner"

def execute(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            partner = json.loads(data)
            partnerId = get_random_id()
            email = partner["email"]
            contact = partner["contact"]
            aadharcard = partner["aadhar"]
            pancard = partner["pancard"]
            partnerExistsByEmail = get_partner_by_email(email)
            partnerExistsByContact = get_partner_by_contact(contact)
            partnerExistsByPancard = get_partner_by_pancard(pancard)
            partnerExistsByAadharCard = get_partner_by_aadharcard(aadharcard)

            if partnerExistsByEmail:
                return{
                    "statusCode":"201",
                    "body": f'Partner with email {email} already exists'
                }
            elif partnerExistsByContact:
                return {
                    "statusCode": "201",
                    "body": f'Partner with contact {contact} already exists'
                }
            
            elif partnerExistsByPancard:
                return {
                    "statusCode": "201",
                    "body": f'Partner with Pancard {pancard} already exists'
                }
            elif partnerExistsByAadharCard:
                return {
                    "statusCode": "201",
                    "body": f'Partner with Aadharcard {aadharcard} already exists'
                }

        return{
            "statuscode":"200",
            "body":200
        }
    except Exception as ex:
        print("Error in Registering Partner")
    return{
        "statusCode":"503",
        "body":"Error"
    }
def get_random_id():
    id=str(uuid.uuid4())
    return id

def get_dynamo():
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    dynamo = boto3.resource("dynamodb")
    dynamoTable = dynamo.Table(table)
    return dynamoTable


def put_data_to_dynamo(partnerId, partnerFname, partnerLname, email, contact, aadharcard, pancard, password):
    dynamoObj = get_dynamo()
    partnername = partnerFname[0:3] + partnerLname[0:3]
    dynamoObj.put_item(
        Item={
            "partnerId":partnerId,
            "partnerFname":partnerFname,
            "partnerLname":partnerLname,
            "partnername": partnername,
            "aadharcard":aadharcard,
            "pancard":pancard,
            "email": email,
            "password":password,
            "active": 0,
            "contact": contact
        }
    )
    return "Success"

def get_partner_by_email(email):
    dynamodb = boto3.client('dynamodb')
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    print(table)
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='email= :email',
            ExpressionAttributeValues={
                ':email':{'S':email}
            }
        )
        print(response)
        return len(response['Items']) > 0
    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False

def get_partner_by_pancard(pancard):
    dynamodb = boto3.client('dynamodb')
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    print(table)
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='pancard= :pancard',
            ExpressionAttributeValues={
                ':pancard':{'S':pancard}
            }
        )
        print(response)
        return len(response['Items']) > 0
    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False

def get_partner_by_aadharcard(aadharcard):
    dynamodb = boto3.client('dynamodb')
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    print(table)
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='aadharcard= :aadharcard',
            ExpressionAttributeValues={
                ':aadharcard':{'S':aadharcard}
            }
        )
        print(response)
        return len(response['Items']) > 0
    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False


def get_partner_by_contact(contact):
    dynamodb = boto3.client('dynamodb')
    table = os.environ.get("AAMHI_UNIQUE_REGISTER_TABLE")
    print(table)
    try:
        response = dynamodb.scan(
            TableName=table,
            FilterExpression='contact= :contact',
            ExpressionAttributeValues={
                ':contact':{'S':contact}
            }
        )
        print(response)
        return len(response['Items']) > 0

    except Exception as e:
        print(f'Error searching DynamoDB table: {e}')
        return False
    
