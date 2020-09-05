import os
import boto3

if __name__ == "__main__":
    print("Python preprocess is running ")
    print("Downloading input image")
    S3_INPUT_BUCKET_NAME = os.environ.get("S3_INPUT_BUCKET_NAME", "ERROR")
    S3_INPUT_OBJECT_NAME = os.environ.get("S3_INPUT_OBJECT_NAME", "ERROR")
    print(S3_INPUT_BUCKET_NAME, S3_INPUT_OBJECT_NAME)

    s3 = boto3.client("s3")
    with open("input_data/input-image.dat", "wb") as f:
        s3.download_fileobj(S3_INPUT_BUCKET_NAME, "S3_INPUT_OBJECT_NAME", f)

    print("S3 DOWNLOAD COMPLETED")
