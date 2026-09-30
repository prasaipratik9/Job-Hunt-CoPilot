"""
Days 5-7 - Job Hunt Copilot
Stage 2 of the pipeline: match_resume()

Embeds each resume chunk and each requirement using Titan Text
Embeddings V2, then scores every (requirement, chunk) pair with cosine
similarity. For each requirement, this returns the resume chunk(s)
that best support it, which is what score_fit() will use next.

Auth: boto3 reads the AWS_BEARER_TOKEN_BEDROCK environment variable.
"""

import json

import boto3
from botocore.exceptions import ClientError

from resume_chunker import load_resume, chunk_resume
from extract_requirements import extract_requirements

REGION = "us-east-1"
EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"
DIMENSIONS = 512  # AWS: ~99% of 1024-dim accuracy, half the storage
RESUME_FILE = "Pratik Prasai.txt"
POSTING_FILE = "job_posting_1.txt"
TOP_K = 2  # how many resume chunks to keep per requirement


def embed_text(client, text):
    """
    Turn one piece of text into a Titan V2 embedding: a list of
    DIMENSIONS floats. normalize=True means the vector's length is
    scaled to 1, which is what lets a plain dot product double as
    cosine similarity in cosine_similarity() below.
    """
    body = json.dumps({
        "inputText": text,
        "dimensions": DIMENSIONS,
        "normalize": True,
    })
    response = client.invoke_model(
        modelId=EMBED_MODEL_ID,
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]


def embed_chunks(client, chunks):
    """Add an 'embedding' key to each resume chunk dict, in place."""
    for chunk in chunks:
        chunk["embedding"] = embed_text(client, chunk["text"])
    return chunks


def cosine_similarity(vec_a, vec_b):
    """
    Dot product of two vectors. Since both come from embed_text() with
    normalize=True, each vector's length is already 1, so this dot
    product IS the cosine similarity, no division needed.
    """
    return sum(a * b for a, b in zip(vec_a, vec_b))


def match_resume(client, requirements, chunks, top_k=TOP_K):
    """
    For each requirement, embed its text and compare it against every
    resume chunk's embedding. Returns requirements with a new
    'top_matches' list: the top_k chunks by similarity score, richest
    match first.
    """
    matched = []
    for req in requirements:
        req_embedding = embed_text(client, req["text"])

        scored_chunks = []
        for chunk in chunks:
            score = cosine_similarity(req_embedding, chunk["embedding"])
            scored_chunks.append({
                "chunk_id": chunk["id"],
                "text": chunk["text"],
                "score": round(score, 4),
            })

        scored_chunks.sort(key=lambda c: c["score"], reverse=True)

        matched.append({
            **req,
            "top_matches": scored_chunks[:top_k],
        })
    return matched


def main():
    client = boto3.client("bedrock-runtime", region_name=REGION)

    try:
        resume_text = load_resume(RESUME_FILE)
        chunks = chunk_resume(resume_text)
        print(f"Chunked resume into {len(chunks)} pieces. Embedding...")
        embed_chunks(client, chunks)

        posting_text = load_resume(POSTING_FILE)  # same plain text loader
        requirements = extract_requirements(client, posting_text)
        print(f"Extracted {len(requirements)} requirements. Matching...\n")

        matched = match_resume(client, requirements, chunks)
    except ClientError as err:
        error = err.response["Error"]
        print(f"Bedrock call failed: {error['Code']} - {error['Message']}")
        return

    for req in matched:
        print(f"REQUIREMENT ({req['priority']}): {req['text']}")
        for m in req["top_matches"]:
            preview = m["text"][:80]
            print(f"  score {m['score']}  chunk[{m['chunk_id']}]  {preview}...")
        print()


if __name__ == "__main__":
    main()
