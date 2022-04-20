import boto3
import sys
import moto
import pytest
from dotenv import load_dotenv
import os

def check_env():
    if sys.version[:3] != "3.8":
        print("Wrong Python version.")
        return False
    if boto3.__version__ != "1.14.15":
        print("Wrong boto3 version.")
        return False
    if moto.__version__ != "1.3.15.dev.965":
        print("Wrong moto version.")
        return False
    if pytest.__version__ != "5.4.3":
        print("Wrong pytest version.")
        return False
    return True

def load_credentials():
    load_dotenv()

class Client(object):
    isConnected = False
    boto = None
    dynamo = None
    exceptions = None
    table = None
    

    __instance=None
    def __new__(cls):
        if Client.__instance is None:
            Client.__instance = object.__new__(cls)

        return Client.__instance

    def instantiate(cls):
        load_credentials()
        cls.boto = boto3.client('dynamodb',
                                aws_access_key_id=os.environ.get("AWS_ID"),
                                aws_secret_access_key=os.environ.get("AWS_PASS"),
                                region_name=os.environ.get("REGION"))

        cls.dynamo = boto3.resource('dynamodb',
                                    aws_access_key_id=os.environ.get("AWS_ID"),
                                    aws_secret_access_key=os.environ.get("AWS_PASS"),
                                    region_name=os.environ.get("REGION"))

        cls.exceptions = cls.boto.exceptions
        print("successful Instantiation...")

    def create_table(cls,name):
        try:
            table = cls.dynamo.create_table(
                TableName=name,
                KeySchema=[
                    {
                        'AttributeName': 'Id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'Id',
                        'AttributeType': 'S'
                    }
    
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            print("creating table...")
            table.wait_until_exists()
            print("table created")
    
        except cls.exceptions.ResourceInUseException:
            print("table already exists.")


    def delete_table(cls,name):
        try:
            print("deleting table...")
            cls.table = cls.dynamo.Table(name)
            cls.table.delete()
            cls.table.wait_until_not_exists()
            print("table deleted")
        except cls.exceptions.ResourceNotFoundException:
            print("this table doesn't exist, can't be deleted")


    def select_table(cls,name):
        try:
            cls.table = cls.dynamo.Table(name)
        except cls.exceptions.ResourceNotFoundException:
            print("this table doesn't exist")

    def get_item(cls, id):
        result = cls.table.get_item(Key={'Id' : id})
        return result['Item']

    def put_item(cls,key,item):
        item['Id'] = key
        output = cls.table.put_item(Item=item)
        return output

        
             








