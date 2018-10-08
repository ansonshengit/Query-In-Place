# Query-In-Place
AWS supports a robust suite of tools and services that makes analyzing and processing large amounts of data in the cloud faster and more efficient. In this builders session, AWS storage and data experts guide you through Amazon S3, Amazon Glacier, and our query-in-place services such as Amazon S3 Select, Amazon Glacier Select, Amazon Athena, and Amazon Redshift Spectrum. We also provide best practices around using them with other analytics services like Amazon EMR and AWS Glue to build data lakes and deploy other analytics solutions. 

This document proivdes the instruction for AWS builder session.
Understanding of a data lake construct, AWS S3 Select, Glacier Select, Athena and Glue is recommended. 

# Section 1 - S3 Select and Glacier Select

Sample Data Description: Two CSV files which contains a list of airport name, code, location. One small size, 6M, with ~50k rows of records. Another large file, 500M, with 4 millions rows of records. 

Sample File Location: airport-code-small.csv and airport-code-large.csv stored in <<Bucket Name>> of AWS us-east-1 region. 

## S3 Select Builder Instruction:
1. Review the python script provided in this repository, "s3-select-compare-small.py" and "s3-select-compare-large.py". 
2. Create a cloud 9 environment on AWS in us-east-1 region. 
3. Install python SDK boto3 in the cloud 9 IDE (if not already) created in step 2 above. CLI: "sudo pip install boto3". 
4. Run the two python scripts respectively. 
5. Review the results, which shows the significant time imporvement of a query performance with s3 select, the larger the data, the greater the performance. 

## Glacier Select Builder Instruction:
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

Sample Data Description: Example ELB logs which is stored s3://athena-examples/elb/raw/, the format is txt, multiple txt files stored under this s3 location. 

## Create External Table using DDL statement:
1. Launch Athena, and select the database that you wish to create the table in on left panel. It can be the default. 
2. Run the below DDL statement, this should create a table under the selected database, against the sample elb logs. 
``CREATE EXTERNAL TABLE IF NOT EXISTS elb_logs_raw_native (``
`` request_timestamp string,``
``  elb_name string, ``
``  request_ip string, ``
``  request_port int, ``
``  backend_ip string, ``
``  backend_port int, ``
``  request_processing_time double, ``
``  backend_processing_time double, ``
``  client_response_time double, ``
``  elb_response_code string, ``
``  backend_response_code string, ``
``  received_bytes bigint, ``
``  sent_bytes bigint, ``
``  request_verb string, ``
``  url string, ``
``  protocol string, ``
``  user_agent string, ``
``  ssl_cipher string, ``
`` ssl_protocol string ) 
``ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'``
``WITH SERDEPROPERTIES (``
``         'serialization.format' = '1','input.regex' = '([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:\-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \\\"([^ ]*) ([^ ]*) (- |[^ ]*)\\\" (\"[^\"]*\") ([A-Z0-9-]+) ([A-Za-z0-9.-]*)$' ) 
LOCATION 's3://athena-examples/elb/raw/';``

## Run Simple Query:
1. You created a table on the data stored in Amazon S3 and you are now ready to query the data. Run a simple query:

`SELECT * FROM elb_logs_raw_native WHERE elb_response_code = '200' LIMIT 100;`

## Create a External Table which Partitions the data:
The sampel ELB log is stored in time-series formats. Without a partition, Athena scans the entire table while executing queries. With partitioning, you can restrict Athena to specific partitions, thus reducing the amount of data scanned, lowering costs, and improving performance.
Athena uses Apache Hive–style data partitioning.  You can partition your data across multiple dimensions―e.g., month, week, day, hour, or customer ID―or all of them together.
To use partitions, you first need to change your schema definition to include partitions, then load the partition metadata in Athena. Use the same CREATE TABLE statement but with partitioning enabled:

1. Run DDL statement:
`CREATE EXTERNAL TABLE IF NOT EXISTS elb_logs_raw_native_part (
  request_timestamp string, 
  elb_name string, 
  request_ip string, 
  request_port int, 
  backend_ip string, 
  backend_port int, 
  request_processing_time double, 
  backend_processing_time double, 
  client_response_time double, 
  elb_response_code string, 
  backend_response_code string, 
  received_bytes bigint, 
  sent_bytes bigint, 
  request_verb string, 
  url string, 
  protocol string, 
  user_agent string, 
  ssl_cipher string, 
  ssl_protocol string ) 
PARTITIONED BY(year string, month string, day string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
         'serialization.format' = '1','input.regex' = '([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:\-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \\\"([^ ]*) ([^ ]*) (- |[^ ]*)\\\" (\"[^\"]*\") ([A-Z0-9-]+) ([A-Za-z0-9.-]*)$' )
LOCATION 's3://athena-examples/elb/raw/';`

2. Add partition:
`ALTER TABLE elb_logs_raw_native_part ADD PARTITION (year='2015',month='01',day='01') location 's3://athena-examples/elb/raw/2015/01/01/'`

3. Display the partitions created:
`show partitions elb_logs_raw_native_part`

4. Run more efficient query. Now you can restrict each query by specifying the partitions in the WHERE clause. In this case, Athena scans less data and finishes faster. Here is an example:
`SELECT distinct(elb_response_code),
         count(url)
FROM elb_logs_raw_native_part
WHERE year='2015'
        AND month= '01'
        AND day='01'
GROUP BY  elb_response_code`

## Query columnar format
1. Create a table on the Parquet data set. Note that your schema remains the same and you are compressing files using Snappy.
`CREATE EXTERNAL TABLE IF NOT EXISTS elb_logs_pq (
  request_timestamp string,
  elb_name string,
  request_ip string,
  request_port int,
  backend_ip string,
  backend_port int,
  request_processing_time double,
  backend_processing_time double,
  client_response_time double,
  elb_response_code string,
  backend_response_code string,
  received_bytes bigint,
  sent_bytes bigint,
  request_verb string,
  url string,
  protocol string,
  user_agent string,
  ssl_cipher string,
  ssl_protocol string )
PARTITIONED BY(year int, month int, day int) 
STORED AS PARQUET
LOCATION 's3://athena-examples/elb/parquet/'
tblproperties ("parquet.compress"="SNAPPY");`

2. To allow the catalog to recognize all partitions, run msck repair table elb_logs_pq. After the query is complete, you can list all your partitions.

`msck repair table elb_logs_pq`

3. Show partitions:
`show partitions elb_logs_pq`

Comparing performance between querying of the same query between text files and Parquet files
1. Query on Parquet file, compressed, partitioned, and columnar data:
`SELECT elb_name,
       uptime,
       downtime,
       cast(downtime as DOUBLE)/cast(uptime as DOUBLE) uptime_downtime_ratio
FROM 
    (SELECT elb_name,
        sum(case elb_response_code
        WHEN '200' THEN
        1
        ELSE 0 end) AS uptime, sum(case elb_response_code
        WHEN '404' THEN
        1
        ELSE 0 end) AS downtime
    FROM elb_logs_pq
    GROUP BY  elb_name)`
    
2. Query on raw text files:
`SELECT elb_name,
       uptime,
       downtime,
       cast(downtime as DOUBLE)/cast(uptime as DOUBLE) uptime_downtime_ratio
FROM 
    (SELECT elb_name,
        sum(case elb_response_code
        WHEN '200' THEN
        1
        ELSE 0 end) AS uptime, sum(case elb_response_code
        WHEN '404' THEN
        1
        ELSE 0 end) AS downtime
    FROM elb_logs_raw_native
    GROUP BY  elb_name)`



Athena charges you by the amount of data scanned per query. By converting your data to columnar format, compressing and partitioning it, you not only save costs but also get better performance. The following table compares the savings created by converting data into columnar format.
Dataset 	Size on Amazon S3 	Query Run time 	Data Scanned 	Cost
Data stored as text files 	1 TB 	236 seconds 	1.15 TB 	$5.75
Data stored in Apache Parquet format* 	130 GB 	6.78 seconds 	2.51 GB 	$0.013
Savings / Speedup 	87% less with Parquet 	34x faster 	99% less data scanned 	99.7% savings

(*compressed using Snappy compression)
