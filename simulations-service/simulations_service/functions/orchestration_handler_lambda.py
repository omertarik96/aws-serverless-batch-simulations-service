import logging
import json
import os
import boto3
import uuid

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

TABLE_NAME = os.environ.get("TABLE_NAME")

# These might be available next time we run this function
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    """
    Create unique job id and write 10 jobs to DynamoDB
    """
    LOG.info(f"EVENT: {json.dumps(event)}")

    for record in event["Records"]:
        if record["s3"]:
            s3_bucket_name = record["s3"]["bucket"]["name"]
            object_key = record["s3"]["object"]["key"]
            LOG.info(f"S3_INPUT_BUCKET_NAME {s3_bucket_name}")
            LOG.info(f"S3_INPUT_OBJECT_KEY {object_key}")

            try:
                unique_job_id = str(uuid.uuid4())
                for i in range(1, 11):
                    write_new_job_to_table(unique_job_id, i, s3_bucket_name, object_key)

                return {
                    "statusCode": 200,
                    "body": "Hello to Sd! Everything went smooth :)",
                }

            except Exception as exception:
                LOG.error(exception)
                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        {
                            "message": "An error happened. We are sorry, please let us know"
                        }
                    ),
                }


def write_new_job_to_table(
    job_id, job_number, s3_input_bucket_name, s3_input_object_name
):
    """Write new job to table with status as new"""
    pk = f"{job_id}#{job_number}"
    status = "NEW"
    response = table.put_item(
        Item={
            "PK": pk,
            "status": status,
            "s3_input_bucket_name": s3_input_bucket_name,
            "s3_input_object_name": s3_input_object_name,
        }
    )
    LOG.info(f"New Job Write Response: {json.dumps(response)}")
