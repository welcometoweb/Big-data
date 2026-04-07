import json

def lambda_handler(event, context):
    print("🔥 Lambda triggered successfully!")

    print("📥 Event received:")
    print(json.dumps(event, indent=2))

    return {
        "statusCode": 200,
        "body": json.dumps("Lambda is working through CICD")
    }
