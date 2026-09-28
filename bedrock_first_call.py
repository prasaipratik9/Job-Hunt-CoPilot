"""
Day 3-4 - Job Hunt Copilot
First direct call to Amazon Bedrock using the Converse API.
Prints the raw response so you can see exactly what comes back,
then pulls out the reply text and token usage.

Auth: boto3 reads the AWS_BEARER_TOKEN_BEDROCK environment variable
automatically, so no key ever appears in this file.
"""

import json

import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"
MODEL_ID = "amazon.nova-micro-v1:0"  # cheapest tier, fine for iteration

PROMPT = (
    "In two sentences, explain what a job posting's 'must-have' "
    "requirements are and why they matter when tailoring a resume."
)


def call_model(client, prompt):
    """Send one user message to the model and return the full response dict."""
    return client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 200, "temperature": 0.2},
    )


def main():
    client = boto3.client("bedrock-runtime", region_name=REGION)

    try:
        response = call_model(client, PROMPT)
    except ClientError as err:
        error = err.response["Error"]
        print(f"Bedrock call failed: {error['Code']} - {error['Message']}")
        return

    print("=== RAW RESPONSE ===")
    print(json.dumps(response, indent=2, default=str))

    reply = response["output"]["message"]["content"][0]["text"]
    usage = response["usage"]

    print("\n=== REPLY TEXT ===")
    print(reply)

    print("\n=== TOKEN USAGE ===")
    print(f"Input tokens:  {usage['inputTokens']}")
    print(f"Output tokens: {usage['outputTokens']}")


if __name__ == "__main__":
    main()
