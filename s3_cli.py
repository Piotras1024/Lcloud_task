import argparse
import boto3
import re


def list_files(bucket_name, prefix=''):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')

    print(f"Listing files in bucket '{bucket_name}' with prefix '{prefix}':\n")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            print(obj['Key'])


def upload_file(bucket_name, file_path, s3_key):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")


def list_files_with_filter(bucket_name, prefix='', pattern=''):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    regex = re.compile(pattern)

    print(f"Listing files in bucket '{bucket_name}' with prefix '{prefix}' matching pattern '{pattern}':\n")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if regex.search(key):
                print(key)


def delete_files_with_filter(bucket_name, prefix='', pattern=''):
    s3 = boto3.client('s3')
    regex = re.compile(pattern)
    objects_to_delete = []

    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if regex.search(key):
                objects_to_delete.append({'Key': key})

    if objects_to_delete:
        response = s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})
        deleted = response.get('Deleted', [])
        print(f"Deleted {len(deleted)} objects:")
        for obj in deleted:
            print(obj['Key'])
    else:
        print("No objects matched the pattern.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='S3 CLI Tool')
    subparsers = parser.add_subparsers(dest='command')

    # List files command
    list_parser = subparsers.add_parser('list', help='List all files in the S3 bucket')
    list_parser.add_argument('--bucket', required=True, help='Name of the S3 bucket')
    list_parser.add_argument('--prefix', default='', help='Prefix to filter objects')

    # Upload local file
    upload_parser = subparsers.add_parser('upload', help='Upload a file to the S3 bucket')
    upload_parser.add_argument('--bucket', required=True, help='Name of the S3 bucket')
    upload_parser.add_argument('--file', required=True, help='Local file path to upload')
    upload_parser.add_argument('--key', required=True, help='S3 object key for the uploaded file')

    # List files with filter command
    filter_parser = subparsers.add_parser('list-filter', help='List files matching a regex filter')
    filter_parser.add_argument('--bucket', required=True, help='Name of the S3 bucket')
    filter_parser.add_argument('--prefix', default='', help='Prefix to filter objects')
    filter_parser.add_argument('--pattern', required=True, help='Regex pattern to match object keys')

    # Delete files command
    delete_parser = subparsers.add_parser('delete', help='Delete files matching a regex filter')
    delete_parser.add_argument('--bucket', required=True, help='Name of the S3 bucket')
    delete_parser.add_argument('--prefix', default='', help='Prefix to filter objects')
    delete_parser.add_argument('--pattern', required=True, help='Regex pattern to match object keys')


    # Parsing arguments
    args = parser.parse_args()

    # Checking what command was given and calling the appropriate function
    if args.command == 'list':
        list_files(args.bucket, args.prefix)
    elif args.command == 'upload':
        upload_file(args.bucket, args.file, args.key)
    elif args.command == 'list-filter':
        list_files_with_filter(args.bucket, args.prefix, args.pattern)
    elif args.command == 'delete':
        delete_files_with_filter(args.bucket, args.prefix, args.pattern)
    else:
        parser.print_help()



## 1. list_files start - python s3_cli.py list --bucket developer-task2 --prefix TIE-rp/
## 2. upload files start - python s3_cli.py upload --bucket developer-task2 --file lcloud_task_file.txt --key TIE-rp/lcloud_task_file.txt

## 3. list an AWS bucket files taht match a "filter" regex
## Example use

## a. python s3_cli.py list-filter --bucket developer-task2 --prefix TIE-rp/ --pattern '.*test.*'
## filter all files with word "upload"

## b. python s3_cli.py list-filter --bucket developer-task2 --prefix TIE-rp/ --pattern '.*upload.*'
## filter all files with word "upload"

## c. python s3_cli.py list-filter --bucket developer-task2 --prefix TIE-rp/ --pattern '.*/test.*'
## filter all files that start with "test"

## 4. python s3_cli.py delete --bucket developer-task2 --prefix TIE-rp/ --pattern '.*/test.*'
## above delete commend will delete all the files wich start with word "test"

