# Query-In-Place Workshop

This document proivdes the instruction for AWS builder session.
Understanding of a data lake construct, AWS S3 Select, Glacier Select, Athena and Glue is recommended. 

AWS Accounts:
*.c builder1 https://464361240967.signin.aws.amazon.com/console
*.c builder2 https://725012194027.signin.aws.amazon.com/console
*.c builder3 https://606504329419.signin.aws.amazon.com/console
*.c builder4 https://245730503502.signin.aws.amazon.com/console
*.c builder5 https://485158749081.signin.aws.amazon.com/console


# Section 1 - S3 Select and Glacier Select

Sample Data Description: Two CSV files which contains a list of airport name, code, location, etc. 
1. One small size file, 6M, with ~50k rows of records. 
2. Another large size file, 500M, with 4 millions rows of records. 

Sample File Location: The two files are available in s3 bucket your builder account: builder<x>-us-east-1 (replace x with your builder number). 

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
4. Before running the script, create a vault in us-east-1 region. Purchase one provisioned capacity. Record the vault name for input to the python script. Enable the vault notification via SNS. In interest of time, this step is pre-loaded.
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

6. Create a glacier select output bucket in us-east-1 region. Record the bucket name and bucket prefix for input to the python script. In interest of time, this step is pre-loaded.

7. Create a lambda function with the lambda scrip provided. The attached IAM role require lambda execution, S3 full access, and Glacier full access. Configure the lambda trigger to the be SNS of the Glacier Vault notification, which was created previously. Configure the lambda memory to max. Configure the output bucket name and object key. In interest of time, this step is pre-loaded.

8. Run the python script "glacier-select-compare-large", the code will do two things, the first part of the code initiates a "archive-retrieval" job, which will trigger the lambda via SNS once the archive is ready for download, Lambda function will download the file and copy to the output bucket and prefix defined previously. The second part of the code will do Glacier Select and only initiate a job only to retrieve the relevant data of the object and generate the outcome to the bucket location define in the python script. 
9. Review the results, which shows in the s3 bucket, one result would have the whole object retrieved and the other result showing only the relevant data retrieved, with much smaller file size. 

# Section 2 - Athena

Sample Data Description: Example ELB logs which is stored s3://athena-examples/elb/raw/, the format is txt, multiple txt files stored under this s3 location. 

Another Sample data location: s3://aws-glue-datasets-us-east-1/examples/

 s3://aws-bigdata-blog/artifacts/glue-data-lake/data/
 s3://serverless-analytics/glue-blog

https://s3.console.aws.amazon.com/s3/buckets/aws-glue-datasets-us-east-1/examples/?region=us-east-1&tab=overview


## Create External Table using DDL statement:
1. Launch Athena, and select the database that you wish to create the table in on left panel. It can be the default. 
2. Run the below DDL statement, this should create a table under the selected database, against the sample elb logs. 
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS elb_logs_raw_native (
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
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
         'serialization.format' = '1','input.regex' = '([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:\-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \\\"([^ ]*) ([^ ]*) (- |[^ ]*)\\\" (\"[^\"]*\") ([A-Z0-9-]+) ([A-Za-z0-9.-]*)$' ) 
LOCATION 's3://athena-examples/elb/raw/';
```

## Run Simple Query:
1. You created a table on the data stored in Amazon S3 and you are now ready to query the data. Run a simple query:

```sql
SELECT * FROM elb_logs_raw_native WHERE elb_response_code = '200' LIMIT 100;
```

## Create a External Table which Partitions the data:
The sampel ELB log is stored in time-series formats. Without a partition, Athena scans the entire table while executing queries. With partitioning, you can restrict Athena to specific partitions, thus reducing the amount of data scanned, lowering costs, and improving performance.
Athena uses Apache Hive–style data partitioning.  You can partition your data across multiple dimensions―e.g., month, week, day, hour, or customer ID―or all of them together.
To use partitions, you first need to change your schema definition to include partitions, then load the partition metadata in Athena. Use the same CREATE TABLE statement but with partitioning enabled:

1. Run DDL statement:
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS elb_logs_raw_native_part (
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
LOCATION 's3://athena-examples/elb/raw/';
```

2. Add partition:
```sql
ALTER TABLE elb_logs_raw_native_part ADD PARTITION (year='2015',month='01',day='01') location 's3://athena-examples/elb/raw/2015/01/01/'
```

3. Display the partitions created:
```sql
show partitions elb_logs_raw_native_part
```

4. Run more efficient query. Now you can restrict each query by specifying the partitions in the WHERE clause. In this case, Athena scans less data and finishes faster. Here is an example:
```sql
SELECT distinct(elb_response_code),
         count(url)
FROM elb_logs_raw_native_part
WHERE year='2015'
        AND month= '01'
        AND day='01'
GROUP BY  elb_response_code
```

## Query columnar format
1. Create a table on the Parquet data set. Note that your schema remains the same and you are compressing files using Snappy.
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS elb_logs_pq (
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
tblproperties ("parquet.compress"="SNAPPY");
```

2. To allow the catalog to recognize all partitions, run msck repair table elb_logs_pq. After the query is complete, you can list all your partitions.

```sql
msck repair table elb_logs_pq
```

3. Show partitions:
```sql
show partitions elb_logs_pq
```

Comparing performance between querying of the same query between text files and Parquet files
1. Query on Parquet file, compressed, partitioned, and columnar data:
```sql
SELECT elb_name,
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
    GROUP BY  elb_name)
```
    
2. Query on raw text files:
```sql
SELECT elb_name,
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
    GROUP BY  elb_name)
```



Athena charges you by the amount of data scanned per query. By converting your data to columnar format, compressing and partitioning it, you not only save costs but also get better performance. The following table compares the savings created by converting data into columnar format.
Dataset 	Size on Amazon S3 	Query Run time 	Data Scanned 	Cost
Data stored as text files 	1 TB 	236 seconds 	1.15 TB 	$5.75
Data stored in Apache Parquet format* 	130 GB 	6.78 seconds 	2.51 GB 	$0.013
Savings / Speedup 	87% less with Parquet 	34x faster 	99% less data scanned 	99.7% savings

(*compressed using Snappy compression)
