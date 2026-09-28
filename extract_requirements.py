"""
Days 5-7 - Job Hunt Copilot
Stage 1 of the pipeline: extract_requirements()

Takes the plain text of a job posting, asks Bedrock to pull out the
requirements, and returns them as a Python list of dicts, each tagged
"must-have" or "nice-to-have". score_fit() will weight on that tag later.

Auth: boto3 reads the AWS_BEARER_TOKEN_BEDROCK environment variable.
"""

import json

import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"
MODEL_ID = "amazon.nova-lite-v1:0"
POSTING_FILE = "job_posting_2.txt"
VALID_PRIORITIES = {"must-have", "nice-to-have"}

SYSTEM_PROMPT = """You extract candidate requirements from job postings.
List only things a candidate must bring: skills, tools, technologies,
experience, qualifications, and knowledge. Do NOT include the job title,
the company description, location, benefits, perks, team culture, or
the impact the role has. Keep each requirement short and specific.

If a requirement has examples or names in brackets, keep them in the
text. For example, "protocol knowledge (Model Context Protocol or
similar)" should become "protocol knowledge such as Model Context
Protocol", not just "protocol knowledge".

The posting may end with an "Employer questions" section. First,
extract requirements from the whole main posting as described above,
since that is the most important part. Then, additionally, turn
questions that name a specific skill, tool, or role into must-have
requirements. For example, "Do you have Rust experience?" becomes
"Rust experience", and "How many years' experience do you have as a
Data Steward?" becomes "experience as a Data Steward". Skip questions
that name no specific skill (such as "Which programming languages are
you experienced in?") and skip questions about right to work, salary,
notice period, and working from home. The questions must never replace
the requirements from the main posting. Only include requirements that
are actually stated in the posting. Never copy examples from these
instructions into your answer.

Tag each one:
- "must-have" if the posting says required, essential, or must
- "nice-to-have" if it says desirable, preferred, bonus, or advantageous
If the posting does not say, treat it as "must-have".

Respond with ONLY valid JSON in exactly this shape, with no extra text:
{"requirements": [{"text": "short requirement", "priority": "must-have"}]}"""


def load_text(file_path):
    """Read a text file and return its contents as one string."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def call_model(client, posting_text):
    """Send the posting to Bedrock with the system prompt, return the reply text."""
    response = client.converse(
        modelId=MODEL_ID,
        system=[{"text": SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": posting_text}]}],
        inferenceConfig={"maxTokens": 1500, "temperature": 0.0},
    )
    return response["output"]["message"]["content"][0]["text"]


def parse_requirements(reply_text):
    """
    Turn the model's reply into a validated list of requirement dicts.
    Models sometimes wrap JSON in ```json fences, so strip those first.
    Raises ValueError if the reply isn't the shape we asked for.
    """
    cleaned = reply_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    data = json.loads(cleaned)
    items = data["requirements"]

    requirements = []
    for item in items:
        text = str(item["text"]).strip()
        priority = str(item["priority"]).strip().lower()
        if priority not in VALID_PRIORITIES:
            priority = "must-have"
        if text:
            requirements.append({"text": text, "priority": priority})
    return requirements


def extract_requirements(client, posting_text):
    """Full stage: posting text in, list of tagged requirements out."""
    reply_text = call_model(client, posting_text)
    try:
        return parse_requirements(reply_text)
    except (json.JSONDecodeError, KeyError, TypeError) as err:
        print(f"Could not parse model reply ({err}). Raw reply was:\n")
        print(reply_text)
        return []


def main():
    posting_text = load_text(POSTING_FILE)
    client = boto3.client("bedrock-runtime", region_name=REGION)

    try:
        requirements = extract_requirements(client, posting_text)
    except ClientError as err:
        error = err.response["Error"]
        print(f"Bedrock call failed: {error['Code']} - {error['Message']}")
        return

    must = [r for r in requirements if r["priority"] == "must-have"]
    nice = [r for r in requirements if r["priority"] == "nice-to-have"]

    print(f"Found {len(requirements)} requirements "
          f"({len(must)} must-have, {len(nice)} nice-to-have)\n")
    for i, req in enumerate(requirements):
        print(f"[{i}] ({req['priority']}) {req['text']}")

    print("\n=== AS JSON ===")
    print(json.dumps(requirements, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
