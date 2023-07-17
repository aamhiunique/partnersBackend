import json
import os
import boto3
import uuid

TAG="Register Aamhi unique Partner"
dynamodb = boto3.client('dynamodb')
table = os.environ.get("AAMHI_UNIQUE_PARTNER_REGISTER_TABLE")
def execute(event, context):
    try:
        if "body" in event.keys():
            data = event["body"]
            partner = json.loads(data)
            partnerId = get_random_id()
            partnerFname = partner["partnerFname"]
            partnerLname = partner["partnerLname"]
            partnerEmail = partner["partnerEmail"]
            partnerContact = partner["partnerContact"]
            partnerPassword = partner["partnerPassword"]
            aadharcard = partner["aadhar"]
            pancard = partner["pan"]

            partnerExistsByEmail = get_partner_by_email(partnerEmail)
            partnerExistsByContact = get_partner_by_contact(partnerContact)
            partnerExistsByPancard = get_partner_by_pancard(pancard)
            partnerExistsByAadharCard = get_partner_by_aadharcard(aadharcard)

            if partnerExistsByEmail:
                return{
                    "statusCode":"409",
                    "body": f'Partner with email {partnerEmail} already exists'
                }
            elif partnerExistsByContact:
                return {
                    "statusCode": "409",
                    "body": f'Partner with contact {partnerContact} already exists'
                }
            
            elif partnerExistsByPancard:
                return {
                    "statusCode": "409",
                    "body": f'Partner with Pancard {pancard} already exists'
                }
            elif partnerExistsByAadharCard:
                return {
                    "statusCode": "409",
                    "body": f'Partner with Aadharcard {aadharcard} already exists'
                }
            else:
                print(partnerId)
                res = put_data_to_dynamo(partnerId, partnerFname, partnerLname, partnerEmail,partnerContact, partnerPassword, aadharcard, pancard)
                return {
                        "statusCode": "201",
                        "body": "Partner Register Successfully"
                        }
    except Exception as ex:
        
        return {
            "statusCode":"503",
            "body":"Error"
        }
    
def get_random_id():
    id=str(uuid.uuid4())
    return id


def put_data_to_dynamo(partnerId, partnerFname, partnerLname, partnerEmail, partnerContact, partnerPassword,aadharcard,pancard):
    partnerUsername = partnerFname[0:3] + partnerLname[0:3]
    table = os.environ.get("AAMHI_UNIQUE_PARTNER_REGISTER_TABLE")
    dynamo = boto3.resource("dynamodb")
    dynamoTable = dynamo.Table(table)
    dynamoTable.put_item(
        Item={
            "partnerId":partnerId,
            "partnerFname":partnerFname,
            "partnerLname":partnerLname,
            "partnerUsername": partnerUsername,
            "aadharcard":aadharcard,
            "pancard":pancard,
            "partnerEmail": partnerEmail,
            "partnerPassword":partnerPassword,
            "active": 0,
            "partnerContact": partnerContact
        }
    )
    return "Success"

def get_partner_by_email(email): 
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
    
