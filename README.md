# Query-In-Place Workshop

This document proivdes the instruction for AWS builder session.
Understanding of a data lake construct, AWS S3 Select, Glacier Select, Athena and Glue is recommended. 

AWS Accounts:

builder1 **https://464361240967.signin.aws.amazon.com/console**

builder2 **https://725012194027.signin.aws.amazon.com/console**

builder3 **https://606504329419.signin.aws.amazon.com/console**

builder4 **https://245730503502.signin.aws.amazon.com/console**

builder5 **https://485158749081.signin.aws.amazon.com/console**


# Topic 1 - S3 Select and Glacier Select

**Sample Data**: Two CSV files which contains a list of airport name, code, location, etc. 
1. One small size file, 6M, with ~50k rows of records. 
2. Another large size file, 500M, with 4 millions rows of records. 

## S3 Select Builder Instruction:

1. Go to S3 console and find the bucket called **builder[x]-us-west-2**, find the sample data file, and click the tab called **"Select From"**.

2. Tick **"File has header row"**, Run **"Preview"**, as well as the following SQL query:

```sql
select name, municipality  from s3object s where municipality = 'Las Vegas' 
```

3. Launch the pre-created cloud 9 environment on AWS in **us-west-2** Oregon region. 

4. Review the pre-loaded python script, **"s3-select-compare-small.py"** and **"s3-select-compare-large.py"**. 

5. Run the **s3-select-small.py** a couple times to observe the difference between query with and without s3 select. 

6. Run the **s3-select-large.py** a couple times to observe the difference between query with and without s3 select. 

## Glacier Select Builder Instruction:

1. Watch the demo, which shows the difference between normal Glacier retrival and Glacier Select. 

# Topic 2 - Glue and Athena
 
**Sample Data**: Infomation of the rides for the green new york city taxis for the month of January 2017.

Sample File Location: Amazon S3 bucket named **s3://aws-bigdata-blog/artifacts/glue-data-lake/data/**.

## Discover the data as is and query in place

1. Select AWS Glue in AWS console. Choose the **us-west-2** AWS Region. Add a new ddatabase, in Database name, type **nycitytaxi**, and choose Create.

2. Add a table to the database **nycitytaxi** by using a crawler. Choose crawler, add crawler, enter the data source: an Amazon S3 bucket named **s3://aws-bigdata-blog/artifacts/glue-data-lake/data/**. 

4. For IAM role, create a role e.g. **AWSGlueServiceRole-Default**. 

5. For Frequency, choose Run on demand. The crawler can be run on demand or set to run on a schedule.

6. For Database, choose **nycitytaxi**.

7. Review the steps, and choose Finish. The crawler is ready to run. Choose Run it now. When the crawler has finished, one table has been added.

8. Choose Tables in the left navigation pane, and then choose **data**. This screen describes the table, including schema, properties, and other valuable information. You can preview the table. 

9. You can query the data using standard SQL, such as:

```sql 
Select * From "nycitytaxi"."data" limit 10;
```



## Athena New Feature: Creating a Table from Query Results (CTAS)
A CREATE TABLE AS SELECT (CTAS) query creates a new table in Athena from the results of a SELECT statement from another query. Athena stores data files created by the CTAS statement in a specified location in Amazon S3. Try to run below sample queries. 


```sql
CREATE TABLE nyctaxi_new_table AS 
SELECT * 
FROM "data";
```

```sql
CREATE TABLE nyctaxi_new_table_pq
WITH (
      format = 'Parquet',
      parquet_compression = 'SNAPPY')
AS SELECT *
FROM "data";
```

```sql
CREATE TABLE nyctaxi_new_table_pq_snappy
WITH (
      external_location='s3://builder[x]-us-west-2/nyctaxi_pq_snappy',
      format = 'Parquet',
      parquet_compression = 'SNAPPY')
AS SELECT *
FROM "data";
```

-----END-----



