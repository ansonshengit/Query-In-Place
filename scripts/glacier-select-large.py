import boto3
glacier = boto3.client("glacier")
vault_name = 'vault1'
archive_id = '<your archive id>'
output_bucket = '<your bucket>'
output_bucket_prefix = '<your bucket prefix>'

jobParameters = {
    "Type": "archive-retrieval",
    "ArchiveId": archive_id,
    "Tier": "Expedited"
        }


print glacier.initiate_job(vaultName=vault_name, jobParameters=jobParameters)

print ("////////Above is whole object retrieval, below is Glacier Select////////")


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
