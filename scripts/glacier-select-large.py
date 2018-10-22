import boto3
# Define variables.
glacier = boto3.client("glacier")
vault_name = 'builder0-vault1'
archive_id = 'TnsNS4AF_Bo2VkQybTCQHcgoz1PbhKuQoPySP1wu8B_TTlKHkn9pjBizsTNvT0nv4mDGypAZLy36qitLaGWj7G45VyBw_oFR8OUHoIuJZuGfF7lUJh8Spwht4ddN6R7j4lGaOMcoYw'
output_bucket = 'builder0-us-east-1'
output_bucket_prefix = 'glacier-select'

# Submit archive-retieval job for whole object:
jobParameters = {
    "Type": "archive-retrieval",
    "ArchiveId": archive_id,
    "Tier": "Expedited"
        }

print glacier.initiate_job(vaultName=vault_name, jobParameters=jobParameters)

print ("////////Above is whole object retrieval, below is Glacier Select////////")

# Submit Glacier select job to retrieve the subset of the object:
jobParameters = {
    "Type": "select",
    "ArchiveId": archive_id,
    "Tier": "Expedited",
    "SelectParameters": {
        "InputSerialization": {
            "csv": {
                        'FileHeaderInfo': 'USE',
                    }
            },
    "ExpressionType": "SQL",
    "Expression": "SELECT * FROM archive WHERE municipality ='Las Vegas'",
    "OutputSerialization": {
        "csv": {}
    }
    },
        "OutputLocation": {
        "S3": {"BucketName": output_bucket, "Prefix": output_bucket_prefix}
        }
}

print glacier.initiate_job(vaultName=vault_name, jobParameters=jobParameters)
