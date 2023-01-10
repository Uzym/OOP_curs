import boto3
from botocore.exceptions import ClientError
import tokens3

class s3Handler:
    
    def __init__(self):
        self.access_key = tokens3.access_key
        self.acess_secret_key = tokens3.acess_secret_key
        self.bucket_name = tokens3.bucket_name
        self.bucket_input_path = tokens3.bucket_input_path
        self.bucket_output_path = tokens3.bucket_output_path
        self.client = boto3.client("s3",
                                   aws_access_key_id=self.access_key,
                                   aws_secret_access_key=self.acess_secret_key)
    
    def upload(self, file_path):

        try:
            self.client.upload_file(
                file_path,
                self.bucket_name,
                self.bucket_input_path + file_path.split('/')[-1]
            )

        except ClientError as e:
            print("Client error")
            print(e)
            
        except Exception as e:
            print(e)

    def download(self, file_path):

        try:
            self.client.download_file(
                self.bucket_name,
                file_path,
                self.bucket_output_path + file_path.split('/')[-1]
            )
        except ClientError as e:
            print("Client error")
            print(e)
        except Exception as e:
            print(e)