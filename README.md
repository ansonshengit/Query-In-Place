# query-in-place
This is for builder session. 

# Section 1 - S3 Select and Glacier Select

Sample Data Description: Two CSV files which contains a list of airport name, code, location. One small size, 6M, with ~50k rows of records. Another large file, 500M, with 4 millions rows of records. 

Sample File Location: airport-code-small.csv and airport-code-large.csv stored in <<Bucket Name>> of AWS us-east-1 region. 

Builder Instruction for S3 Select:
1. Review the python script provided in this repository, "s3-select-compare-small.py" and "s3-select-compare-large.py". 
2. Create a cloud 9 environment on AWS in us-east-1 region. 
3. Install python SDK boto3 in the cloud 9 IDE created in step 2 above. CLI: "sudo pip install boto3". 
4. Run the two python scripts respectively. 
5. Review the results, which shows the significant imporvement of a query performance with s3 select, the larger the data, the greater the performance. 

Builder Instruction for Glacier Select:
1. Review the python script provided in this repository, "glacier-select-compare-small.py" and "glacier-select-compare-large.py". 
2. Create a cloud 9 environment on AWS in us-east-1 region. 
3. Install python SDK boto3 in the cloud 9 IDE created in step 2 above. CLI: "sudo pip install boto3". 
4. Before running the code, you need to create a vault or use a exisitng vault in your AWS account. 
Run the two python scripts respectively. 
5. Review the results, which shows the significant imporvement of a query performance with s3 select, the larger the data, the greater the performance. 

# Section 2 - Athena and Glue


