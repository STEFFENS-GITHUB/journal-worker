import json
import os

import boto3

VERIFY_API_URL = os.getenv("VERIFY_API_URL", "http://localhost:8000/verify-email")
QUEUE_URL = os.environ["EMAIL_VERIFICATION_QUEUE_URL"]


def main():
    sqs = boto3.client(
        "sqs",
        endpoint_url=os.getenv("SQS_ENDPOINT_URL") or None,
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    while True:
        result = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=10, WaitTimeSeconds=20)
        for message in result.get("Messages", []):
            body = json.loads(message["Body"])
            # TODO: send this URL to body["email"] instead of printing it
            print(f"{VERIFY_API_URL}?token={body['token']}", flush=True)
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message["ReceiptHandle"])


if __name__ == "__main__":
    main()
