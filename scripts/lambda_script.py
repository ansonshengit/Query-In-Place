from __future__ import print_function
import json
import boto3
print('Loading function')

def lambda_handler(event, context):
#    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    parsed_message = json.loads(message)
    
    myjobId = parsed_message['JobId']
    print("Original Message" + message)
    print("/////////////Line Divider///////////////")
    print(parsed_message)
    print("/////////////Line Divider///////////////")
    print("Job ID:" + myjobId)

    if parsed_message['Action'] == "ArchiveRetrieval":
        glacier = boto3.client("glacier")
        s3 = boto3.client("s3")

        response = glacier.get_job_output(
        vaultName='vault1',
        jobId=myjobId,
        )

        data = response['body'].read()

        s3.put_object(Body=data, Bucket='<your bucket name>', Key='<your object key>')
        print("put object submitted")
    else :
        print("not the right job type")
  
