import json
import boto3
# Define variables
my_vault = 'builder0-vault1'
my_bucket = 'builder0-us-east-1'
my_key = 'glacier-retrieve/glacier-whole-output.csv'

def lambda_handler(event, context):
#   Read the SNS message.
    message = event['Records'][0]['Sns']['Message']
    parsed_message = json.loads(message)
#   Extract the jobID from the message    
    myjobId = parsed_message['JobId']
    print("Original Message" + message)
    print(parsed_message)
    print("Job ID:" + myjobId)
#   If the sns is for archive retrieval, get the job output. 
    if parsed_message['Action'] == "ArchiveRetrieval":
        glacier = boto3.client("glacier")
        s3 = boto3.client("s3")

        response = glacier.get_job_output(
        vaultName=my_vault,
        jobId=myjobId,
        )
#   Read the file body and upload to s3. 
        data = response['body'].read()
        s3.put_object(Body=data, Bucket=my_bucket, Key=my_key)
        print("put object submitted")
    else :
        print("not the right job type")
