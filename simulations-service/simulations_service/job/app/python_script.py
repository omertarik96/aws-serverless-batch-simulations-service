import json
import ast
import os
import boto3
from botocore.exceptions import ClientError
import logging


client = boto3.client("s3")


def get_dictionary_results_from_output_file(file_path):
    file = open(file_path, "r")
    contents = file.read()
    results = ast.literal_eval(contents)
    file.close()
    return results


def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False


def update_simulation_result(
    table_name, unique_job_id, simulation_number, result, dynamodb=None
):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

    table = dynamodb.Table(table_name)

    pk = f"{unique_job_id}#{simulation_number}"

    response = table.update_item(
        Key={"PK": pk},
        UpdateExpression="set #st=:s, porosity=:p, k_lbm=:k",
        ExpressionAttributeValues={
            ":s": "PROCESSED",
            ":p": str(result["Porosity"]),
            ":k": str(result["K_lbm"]),
        },
        ExpressionAttributeNames={"#st": "status"},
        ReturnValues="UPDATED_NEW",
    )
    return response


if __name__ == "__main__":
    print("Python is running ")

    AWS_BATCH_JOB_ID = os.environ.get("AWS_BATCH_JOB_ID", "NOT_SUPPLIED")
    S3_OUTPUT_BUCKET = os.environ.get("S3_OUTPUT_BUCKET", "NOT_SUPPLIED")
    UNIQUE_JOB_ID = os.environ.get("UNIQUE_JOB_ID", "NOT_SUPPLIED")
    SIMULATION_NUMBER = os.environ.get("SIMULATION_NUMBER", "NOT_SUPPLIED")
    TABLE_NAME = os.environ.get("TABLE_NAME", "NOT_SUPPLIED")
    OUTPUT_FILE_NAME = "./output_data/xPerm_LBM.json"

    dictionary_results = get_dictionary_results_from_output_file(OUTPUT_FILE_NAME)
    print(dictionary_results)

    # Save the output to S3
    print("UPLOADING RESULTS TO OUTPUT S3")
    print(f"S3 OUTPUT BUCKET {S3_OUTPUT_BUCKET}")

    OBJECT_NAME = f"{UNIQUE_JOB_ID}/{SIMULATION_NUMBER}/xPerm_LBM.json"

    print(f"S3 OBJECT NAME: {OBJECT_NAME}")

    s3 = boto3.client("s3")
    with open(OUTPUT_FILE_NAME, "rb") as f:
        s3.upload_fileobj(f, S3_OUTPUT_BUCKET, OBJECT_NAME)

    # Save the output to DynamoDB
    try:
        update_simulation_result(
            TABLE_NAME, UNIQUE_JOB_ID, SIMULATION_NUMBER, dictionary_results
        )
    except Exception as exception:
        print(exception)
