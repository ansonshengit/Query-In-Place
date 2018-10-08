# query-in-place
This is for builder session. 

# Section 1 - S3 Select and Glacier Select

Sample Data Description: Two CSV files which contains a list of airport name, code, location. One small size, 6M, with ~50k rows of records. Another large file, 500M, with 4 millions rows of records. 

Sample File Location: airport-code-small.csv and airport-code-large.csv stored in <<Bucket Name>> of AWS us-east-1 region. 

S3 Select Builder Instruction:
1. Review the python script provided in this repository, "s3-select-compare-small.py" and "s3-select-compare-large.py". 
2. Create a cloud 9 environment on AWS in us-east-1 region. 
3. Install python SDK boto3 in the cloud 9 IDE (if not already) created in step 2 above. CLI: "sudo pip install boto3". 
4. Run the two python scripts respectively. 
5. Review the results, which shows the significant time imporvement of a query performance with s3 select, the larger the data, the greater the performance. 

Glacier Select Builder Instruction:
1. Review the python script provided in this repository, "glacier-select-compare-large.py" for running in Cloud 9 IDE and "glacier-get-job-ouput.py" for running in lambda. 
2. Create a cloud 9 environment on AWS in us-east-1 region. 
3. Install python SDK boto3 in the cloud 9 IDE (if not already) created in step 2 above. CLI: "sudo pip install boto3". 
4. Before running the code, you need to create a vault or use a exisitng vault in your AWS account, in us-east-1 region. Record the vault name for input to the python script. Enable the vault notification via SNS. 
5. Upload the sample data file to the vault mentioned in step 4: airport-code-large.csv. Record the archive id for input to the python script. 
6. Create a output bucket in us-east-1 region. Record the bucket name and bucket prefix for input to the python script. 
7. Create a lambda function with the lambda scrip provided. The attached IAM role require lambda execution and S3 full access. Configure the lambda trigger to the be SNS of the Glacier Vault notification, which was created in step 4. Configure the output bucket name and object key. 
8. Run the python script "glacier-select-compare-large", the code will do two things, the first part of the code initiates a "archive-retrieval" job, which will trigger the lambda via SNS once the archive is ready for download, Lambda function will download the file and copy to the output bucket and prefix defined in step 7. The second part of the code will do Glacier Select and only initiate a job only to retrieve the relevant data of the object and generate the outcome to the bucket location define in the python script. 
9. Review the results, which shows in the s3 bucket, one result would have the whole object retrieved and the other result showing only the relevant data retrieved, with much smaller file size. 

# Section 2 - Athena and Glue


