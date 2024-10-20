import argparse
import boto3


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

    # Parsowanie argumentów
    args = parser.parse_args()

    # Sprawdzenie, jaka komenda została podana, i wywołanie odpowiedniej funkcji
    if args.command == 'list':
        list_files(args.bucket, args.prefix)
    elif args.command == 'upload':
        upload_file(args.bucket, args.file, args.key)
    else:
        parser.print_help()



## list_files start - python s3_cli.py list --bucket developer-task2 --prefix TIE-rp/
## upload files start - python s3_cli.py upload --bucket developer-task2 --file lcloud_task_file.txt --key TIE-rp/lcloud_task_file.txt

