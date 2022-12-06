import boto3 as boto
from botocore.exceptions import ClientError
import os
import sys
import logging
from boto3.s3.transfer import TransferConfig


def upload(file_name, bucket="eng130-videos", object_name=None,expiration=3600):
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
    s3 = boto.client('s3')
    try:
        response = s3.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read', 'ContentType': 'video/mp4'})
        print('https://{b}.s3-eu-west-1.amazonaws.com/{o}'.format(b=bucket, o=object_name))
        #response = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': object_name}, ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        print(e)
    print("\nFile uploaded\n")
    
    return response


def download(file_name, bucket, object_name=None):
    """Download a file to an S3 bucket

    :param file_name: File to download
    :param bucket: Bucket to download from
    :param object_name: S3 object name. If not specified then file_name is used
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Download the file
    s3 = boto.client('s3')
    try:
        response = s3.download_file(bucket, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True, response


def create_bucket(bucket_name, region="eu-west-1"):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (eu-west-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'eu-west-1', default is example
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        s3 = boto.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3.create_bucket(Bucket=bucket_name,
                         CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_bucket(bucket, region="eu-west-1"):
    s3 = boto.resource('s3', region_name=region)
    s3.Bucket(bucket).delete()


def delete_file(bucket, object, region="eu-west-1"):
    s3 = boto.client('s3', region_name=region)
    s3.delete_object(Bucket=bucket, Key=object)


def delete_folder(bucket, location):
    s3 = boto.resource('s3')
    for obj in s3.Bucket(bucket).objects.filter(Prefix=location):
        s3.Object(bucket.name, obj.key).delete()


def list_contents(bucket, region="eu-west-1"):
    s3 = boto.resource('s3', region_name=region)
    for my_bucket_object in bucket.objects.all():
        print(my_bucket_object)


def list_buckets():
    # WIP
    # Retrieve the list of existing buckets
    s3 = boto.client('s3')
    response = s3.list_buckets()
    print(response)


def set_threshold(gb_amount):
    GB = 1024 ** 3
    TransferConfig(multipart_threshold=gb_amount*GB)


# build python environment in vm
if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
