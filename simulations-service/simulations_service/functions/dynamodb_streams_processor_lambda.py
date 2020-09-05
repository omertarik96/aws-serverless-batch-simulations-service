import logging
import json
import os
import boto3


LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


S3_OUTPUT_BUCKET = os.environ.get("S3_OUTPUT_BUCKET")
JOB_QUEUE = os.environ.get("JOB_QUEUE")
JOB_DEFINITION = os.environ.get("JOB_DEFINITION")
TABLE_NAME = os.environ.get("TABLE_NAME")
batch = boto3.client("batch")


def handler(event, context):
    """
    Process DynamoDB stream from JobTable to start jobs
    """
    LOG.info(f"EVENT: {json.dumps(event)}")

    try:
        for record in event["Records"]:
            if record["eventName"] == "INSERT":
                LOG.info("INSERT EVENT RECEIVED")

                # Parse the job id and job number
                new_image = record["dynamodb"]["NewImage"]
                pk = new_image["PK"]["S"]
                s3_input_bucket_name = new_image["s3_input_bucket_name"]["S"]
                s3_input_object_name = new_image["s3_input_object_name"]["S"]
                unique_job_id = pk.split("#")[0]
                simulation_number = pk.split("#")[1]

                LOG.info(f"UNIQUE_JOB_ID: {unique_job_id}")
                LOG.info(f"SIMULATION_NUMBER: {simulation_number}")

                # Submit the job

                response = batch.submit_job(
                    jobName=pk.replace("#", "_"),
                    jobQueue=JOB_QUEUE,
                    jobDefinition=JOB_DEFINITION,
                    containerOverrides={
                        "environment": [
                            {"name": "SIMULATION_NUMBER", "value": simulation_number},
                            {"name": "S3_OUTPUT_BUCKET", "value": S3_OUTPUT_BUCKET},
                            {"name": "UNIQUE_JOB_ID", "value": unique_job_id},
                            {"name": "TABLE_NAME", "value": TABLE_NAME},
                            {
                                "name": "S3_INPUT_BUCKET_NAME",
                                "value": s3_input_bucket_name,
                            },
                            {
                                "name": "S3_INPUT_OBJECT_NAME",
                                "value": s3_input_object_name,
                            },
                        ],
                    },
                )

                LOG.info(f"Batch submit response: {response}")

                # Get the result

        return {
            "statusCode": 200,
            "body": "Everything went smooth :)",
        }

    except Exception as exception:
        LOG.error(exception)
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"message": "An error happened. We are sorry, please let us know"}
            ),
        }
