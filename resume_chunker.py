"""
Day 1 - Job Hunt Copilot
Reads a resume text file, splits it into chunks, and prints them as
structured data (a list of dicts). This is the shape match_resume()
will need later for embedding-based RAG (Days 5-7).
"""

def load_resume(file_path):
    """Read the resume file and return its raw text."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_resume(text, min_length=20):
    """
    Split resume text into chunks by blank line (paragraph-style).
    Drops chunks shorter than min_length so stray blank lines or
    single words don't become their own chunk.
    """
    raw_chunks = text.split("\n\n")
    chunks = []
    for i, raw in enumerate(raw_chunks):
        cleaned = raw.strip().replace("\n", " ")
        if len(cleaned) >= min_length:
            chunks.append({
                "id": i,
                "text": cleaned,
                "length": len(cleaned)
            })
    return chunks


def main():
    resume_text = load_resume("Pratik Prasai.txt")
    chunks = chunk_resume(resume_text)

    print(f"Found {len(chunks)} chunks:\n")
    for chunk in chunks:
        print(f"[{chunk['id']}] ({chunk['length']} chars) {chunk['text'][:80]}...")


if __name__ == "__main__":
    main()