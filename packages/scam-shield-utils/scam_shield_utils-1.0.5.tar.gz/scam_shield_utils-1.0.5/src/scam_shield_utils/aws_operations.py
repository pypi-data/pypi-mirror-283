import boto3
from io import BytesIO
from logger_log import log_message

class awsS3Operations:
    def __init__(self, predict_args) -> None:
        self.predict_args = predict_args
        self.aws_access_key = predict_args['aws_access_key']
        self.aws_secret_key = predict_args['aws_secret_key']
        self.env = predict_args['env']
        self.client = None

    def connect(self):
        try:
            if self.env=='local':
                s3 = boto3.client('s3',aws_access_key_id=self.aws_access_key,aws_secret_access_key=self.aws_secret_key)
            else:
                s3 = boto3.client('s3')
            self.client = s3
            log_message('info','S3 Client Created SUccessfully')
            return True
        except Exception as ex:
            log_message('error',f"Unable to connect to S3. Error : {str(ex)}")
            return False
    
    def put_object(self,body = None,bucket = "",key = ""):
        try:
            if self.client:
                self.client.put_object(Body = body, Bucket = bucket , Key = key)
                return True
        except Exception as ex:
            log_message('error',f"Unable to store data in AWS S3. Errors : {str(ex)}")
            return False
        
    def get_object(self,bucket, key):
        content = None
        try:
            response = self.client.get_object(Bucket = bucket, Key=key)
            if response:
                content = response['Body'].read()
            return content
        except Exception as ex:
            log_message('error',f"Unable to get Model file from S3. Error : {str(ex)}")
            return content