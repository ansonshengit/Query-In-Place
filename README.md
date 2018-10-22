# Query-In-Place Workshop

This document proivdes the instruction for AWS builder session.
Understanding of a data lake construct, AWS S3 Select, Glacier Select, Athena and Glue is recommended. 

AWS Accounts:

builder1 https://464361240967.signin.aws.amazon.com/console

builder2 https://725012194027.signin.aws.amazon.com/console

builder3 https://606504329419.signin.aws.amazon.com/console

builder4 https://245730503502.signin.aws.amazon.com/console

builder5 https://485158749081.signin.aws.amazon.com/console


# Section 1 - S3 Select and Glacier Select

Sample Data Description: Two CSV files which contains a list of airport name, code, location, etc. 
1. One small size file, 6M, with ~50k rows of records. 
2. Another large size file, 500M, with 4 millions rows of records. 

Sample File Location: The two files are available in a public s3 bucket: anson-us-east-1.

## S3 Select Builder Instruction:
1. Review the python script provided in this repository, "s3-select-compare-small.py" and "s3-select-compare-large.py". 
2. Launch the pre-created cloud 9 environment on AWS in us-east-1 region. 
3. Run the s3-select-small.py a couple times to observe the difference between query with and without s3 select. 
4. Run the s3-select-large.py a couple times to observe the difference between query with and without s3 select. 
5. Review the results, which shows the significant time imporvement of a query performance with s3 select, the larger the data, the greater the performance. 

## Glacier Select Builder Instruction:
1. Review the python script provided in this repository, "glacier-select-compare-large.py" for running in Cloud 9 IDE and "glacier-get-job-ouput.py" for running in lambda. 
2. Launch the pre-created cloud 9 environment on AWS in us-east-1 region, if not already.
3. Verify that the "glacier-select-compare-large.py" exists in cloud 9 IDE. 
4. Before running the script, create a vault in us-east-1 region. Purchase one provisioned capacity. Record the vault name for input to the python script. Enable the vault notification via SNS. 
5. Upload the sample data file to the vault mentioned in step 4: airport-code-large.csv. Record the archive id for input to the python script. 
E.g. run below CLI to upload a file to Glacier:

`aws glacier upload-archive --vault-name builder0-vault1 --account-id - --body airport-code-large.csv`

The output of the CLI looks like below, which contain the archieveID:

`
{
    "location": "/889111795564/vaults/builder0-vault1/archives/TnsNS4AF_Bo2VkQybTCQHcgoz1PbhKuQoPySP1wu8B_TTlKHkn9pjBizsTNvT0nv4mDGypAZLy36qitLaGWj7G45VyBw_oFR8OUHoIuJZuGfF7lUJh8Spwht4ddN6R7j4lGaOMcoYw",
    "checksum": "da7aac2dc381c0acbe6146d7117f552e09c4e575d116e13ee6dadde5555779b1",
    "archiveId": "TnsNS4AF_Bo2VkQybTCQHcgoz1PbhKuQoPySP1wu8B_TTlKHkn9pjBizsTNvT0nv4mDGypAZLy36qitLaGWj7G45VyBw_oFR8OUHoIuJZuGfF7lUJh8Spwht4ddN6R7j4lGaOMcoYw"
}
`

6. Create a glacier select output bucket in us-east-1 region. Record the bucket name and bucket prefix for input to the python script. 

7. Create a lambda function with the lambda scrip provided. The attached IAM role require lambda execution, S3 full access, and Glacier full access. Configure the lambda trigger to the be SNS of the Glacier Vault notification, which was created previously. Configure the lambda memory to max. Configure the output bucket name and object key. 

8. Run the python script "glacier-select-compare-large", the code will do two things, the first part of the code initiates a "archive-retrieval" job, which will trigger the lambda via SNS once the archive is ready for download, Lambda function will download the file and copy to the output bucket and prefix defined previously. The second part of the code will do Glacier Select and only initiate a job only to retrieve the relevant data of the object and generate the outcome to the bucket location define in the python script. 
9. Review the results, which shows in the s3 bucket, one result would have the whole object retrieved and the other result showing only the relevant data retrieved, with much smaller file size. 

# Section 2 - Glue and Athena


