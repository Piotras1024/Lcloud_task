import argparse
import boto3


def list_files(bucket_name, prefix=''):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')

    print(f"Listing files in bucket '{bucket_name}' with prefix '{prefix}':\n")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            print(obj['Key'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='S3 CLI Tool')
    subparsers = parser.add_subparsers(dest='command')

    # List files command
    list_parser = subparsers.add_parser('list', help='List all files in the S3 bucket')
    list_parser.add_argument('--bucket', required=True, help='Name of the S3 bucket')
    list_parser.add_argument('--prefix', default='', help='Prefix to filter objects')

    # Parsowanie argumentów
    args = parser.parse_args()

    # Sprawdzenie, jaka komenda została podana, i wywołanie odpowiedniej funkcji
    if args.command == 'list':
        list_files(args.bucket, args.prefix)
    else:
        parser.print_help()