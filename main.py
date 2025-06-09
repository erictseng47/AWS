import time
from config import load_config
from utils import *

def main():
    config = load_config('./.env')

    # 2. Initialization
    session = init_aws_session(config)

    # 3. Create EC2, S3, SQS
    ec2, instance_id = create_ec2_instance(session, config['AMI_ID'])
    s3, bucket_name = create_s3_bucket(session, config['REGION'])
    sqs, queue_url = create_sqs_queue(session, config['queue_name'])

    # 4. Wait 1 minute for AWS resource provisioning
    print("\n⏳ Waiting 1 minute for AWS resource provisioning...")
    time.sleep(60)

    # 5. Check the status of EC2, S3, SQS
    print("\n### Checking status of EC2, S3, SQS ###")
    check_ec2_instances(ec2)
    check_s3_buckets(s3)
    check_sqs_queues(sqs)

    # 6. Upload CSE546_YenKai_Tseng.txt to S3
    print("\n### Uploading CSE546_YenKai_Tseng.txt to S3 ###")
    upload_file_to_s3(s3, config['file_path'], bucket_name, config['object_name'])

    # 7. Send a message to SQS
    print("\n### Sending a message to SQS ###")
    send_sqs_message(sqs, queue_url, 'This is a test message')

    # 8. Display how many messages are in SQS
    print("\n### Displaying how many messages are in SQS ###")
    check_sqs_message(sqs, queue_url)

    # 9. Read one message from SQS
    print("\n### Reading one message from SQS ###")
    get_sqs_message_count(sqs, queue_url)

    # 10. Check SQS message count again
    print("\n### Checking SQS message count again ###")
    check_sqs_message(sqs, queue_url)

    # 11. Release resources
    print("\n### Releasing resources ###")
    delete_s3_bucket(s3, bucket_name)
    delete_sqs_queue(sqs, queue_url)
    terminate_ec2(ec2, instance_id)

    # 12. Check the status of EC2, S3, SQS again
    print("\n### Checking status of EC2, S3, SQS again ###")
    check_ec2_instances(ec2)
    check_s3_buckets(s3)
    time.sleep(60)
    check_sqs_queues(sqs)

if __name__ == '__main__':
    main()