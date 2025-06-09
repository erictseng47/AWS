import boto3
import uuid
from datetime import datetime, timezone

# Initialize AWS session
def init_aws_session(config):
    try:
        session = boto3.Session(
            aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY'],
            region_name=config['REGION']
        )
        return session
    except Exception as e:
        print(f"❌ Failed to initialize AWS Session: {e}")
        raise

# Create EC2 instance
def create_ec2_instance(session, ami_id):
    try:
        ec2 = session.resource('ec2')
        instance = ec2.create_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='my_key',
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'App Tier Worker'}]
            }]
        )
        instance_id = instance[0].id
        print(f"✅ Successfully created EC2 instance, ID: {instance_id}")
        return ec2, instance_id
    except Exception as e:
        print(f"❌ Failed to create EC2 instance: {e}")
        raise

# Create S3 bucket
def create_s3_bucket(session, region):
    s3 = session.client('s3')
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    bucket_name = f'cse546-yenkai-tseng-bucket-{timestamp}-{unique_id}'
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket {bucket_name} already exists")
    except s3.exceptions.ClientError:
        try:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
            print(f"✅ Successfully created S3 bucket: {bucket_name}")
        except Exception as e:
            print(f"❌ Failed to create S3 bucket: {e}")
            raise
    return s3, bucket_name

# Create SQS queue
def create_sqs_queue(session, queue_name):
    sqs = session.client('sqs')
    try:
        response = sqs.create_queue(
            QueueName=queue_name,
            Attributes={'DelaySeconds': '0', 'VisibilityTimeout': '30'}
        )
        queue_url = response['QueueUrl']
        print(f"✅ Successfully created SQS queue '{queue_name}'")

        list_response = sqs.list_queues()
        if 'QueueUrls' in list_response:
            for url in list_response['QueueUrls']:
                print("🔗 Existing queue: " + url)
        else:
            print("No existing SQS queues")

        return sqs, queue_url
    except Exception as e:
        print(f"❌ Failed to create SQS queue: {e}")
        raise

# Check EC2 instance status
def check_ec2_instances(ec2):
    response = ec2.meta.client.describe_instances()
    print("Checking EC2 instance status:")
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"✅ EC2 ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

# Check S3 buckets
def check_s3_buckets(s3):
    response = s3.list_buckets()
    print("Checking S3 status:")
    if 'Buckets' in response and response['Buckets']:
        for bucket in response['Buckets']:
            print(f"✅ S3 Bucket: {bucket['Name']}")
    else:
        print("📭 No S3 buckets found")

# Check SQS queues
def check_sqs_queues(sqs):
    response = sqs.list_queues()
    print("Checking SQS status:")
    if 'QueueUrls' in response:
        for url in response['QueueUrls']:
            print(f"✅ SQS Queue URL: {url}")
    else:
        print("📭 No SQS queues found")

# Send a message to SQS
def send_sqs_message(sqs, queue_url, message):
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        MessageAttributes={
            'name': {
                'StringValue': 'test message',
                'DataType': 'String'
            }
        }
    )
    print(f"📨 Successfully sent message to SQS: '{message}'")

# Check how many messages are in the SQS queue
def check_sqs_message(sqs, queue_url):
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    message_count = int(response['Attributes']['ApproximateNumberOfMessages'])
    print(f"📋 There are currently {message_count} messages in the SQS queue")
    return message_count

# Read a message from SQS queue
def get_sqs_message_count(sqs, queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        WaitTimeSeconds=2
    )
    messages = response.get('Messages', [])
    if not messages:
        print("📋 No messages available in the SQS queue")
        return None
    else:
        message = messages[0]
        body = message['Body']
        attributes = message.get('MessageAttributes', {})
        title = attributes.get('name', {}).get('StringValue', 'Untitled')

        print(f"📝 Message Title: {title}")
        print(f"📝 Message Body: {body}")
        return message

# Upload file to S3
def upload_file_to_s3(s3, file_path, bucket_name, object_name):
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"📤 Uploaded {file_path} to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"❌ Failed to upload file: {e}")
        raise

# Terminate EC2 instance
def terminate_ec2(ec2, instance_id):
    try:
        ec2.meta.client.terminate_instances(InstanceIds=[instance_id])
        print(f"🗑️ Terminated EC2 instance {instance_id}")
    except Exception as e:
        print(f"❌ Failed to terminate EC2 instance: {e}")

# Delete S3 bucket and all its contents
def delete_s3_bucket(s3, bucket_name):
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        s3.delete_bucket(Bucket=bucket_name)
        print(f"🗑️ Deleted S3 bucket {bucket_name}")
    except Exception as e:
        print(f"❌ Failed to delete S3 bucket: {e}")

# Delete SQS queue
def delete_sqs_queue(sqs, queue_url):
    try:
        sqs.delete_queue(QueueUrl=queue_url)
        print(f"🗑️ Deleted SQS queue {queue_url}")
    except Exception as e:
        print(f"❌ Failed to delete SQS queue: {e}")