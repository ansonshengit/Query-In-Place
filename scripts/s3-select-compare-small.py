import boto3
import time

s3 = boto3.client('s3')
bucket = 'anson-us-east-1'
key = 'sample-data/airport-code-small.csv'

#query without S3 select
s1 = time.time()
r1 = s3.get_object(Bucket=bucket, Key=key)
contents = r1['Body'].read()
for line in contents.split('\n')[:-1]:
    data = line.split(',')
    if data[7] == 'Las Vegas': print data[2]
e1 = time.time()

print ("////////////Above result is WITHOUT s3 select. Below result is WITH s3 select//////////////")

#query with s3 select
s2 = time.time()
r2 = s3.select_object_content(
    Bucket=bucket,
    Key=key,
    ExpressionType= 'SQL',
    Expression= 'SELECT obj._3 FROM s3Object as obj WHERE obj._8 = \'Las Vegas\'',
    InputSerialization= {
            'CompressionType': 'NONE',
            'CSV':{
                'FileHeaderInfo': 'IGNORE',
                'RecordDelimiter': '\n',
                'FieldDelimiter': ',',
                }
            },
    OutputSerialization= {
                'CSV':{
                    'RecordDelimiter': '\n',
                    'FieldDelimiter': ',',
                }
            }
)
#Print out the result from s3 select.
for event in r2['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        
#Print out s3 select statistics. 
print("S3 Select Stats details bytesScanned: ")
print(statsDetails['BytesScanned'])
print("S3 Select Stats details bytesReturned: ")
print(statsDetails['BytesReturned'])
print("Each query will cost 0.002 USD per GB scanned, plus 0.0007 USD per GB returned.")

e2 = time.time()

#Print out the time used for two quries. 
print("time taken without s3 select", e1 - s1)
print("time taken with s3 select", e2 - s2)
