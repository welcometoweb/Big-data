import json
import boto3

step_client = boto3.client('stepfunctions')

# 🔁 Replace with your actual Step Function ARN
STATE_MACHINE_ARN = "arn:aws:iam::174405733611:role/service-role/StepFunctions-event-bridge-role-j87rb0j4s"


def lambda_handler(event, context):
    print("🔥 Incoming Event:")
    print(json.dumps(event))

    try:
        # Extract S3 details from EventBridge event
        detail = event.get("detail", {})
        bucket = detail["bucket"]["name"]
        key = detail["object"]["key"]

        print(f"📦 File received: {bucket}/{key}")

        # Derive dataset from path
        # Example: incoming/users/file.csv → dataset = users
        parts = key.split("/")
        dataset = parts[1] if len(parts) > 1 else "unknown"

        # Build input payload for Step Function
        input_payload = {
            "bucket": bucket,
            "key": key,
            "dataset": dataset
        }

        print("🚀 Triggering Step Function with payload:")
        print(json.dumps(input_payload))

        response = step_client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            input=json.dumps(input_payload)
        )

        print("✅ Step Function started:", response["executionArn"])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Step Function triggered successfully",
                "executionArn": response["executionArn"]
            })
        }

    except Exception as e:
        print("❌ Error occurred:", str(e))
        raise e
