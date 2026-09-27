\# Job Hunt Copilot — Build Log



\## \[2026-09-27] — Day 1



\*\*Shipped:\*\*

\- Wrote and ran resume\_chunker.py, splits resume into structured chunks (id, text, length)

\- Verified output against real resume, tuned chunking by adding blank lines to SUMMARY

\- Created GitHub repo (public), with README and Python .gitignore



\*\*Learned:\*\*

\- with open() as a context manager for safe file reading

\- String splitting on blank lines to chunk text, plus filtering short chunks by length

\- id in chunk dicts comes from the original unfiltered index, can skip numbers if a chunk is dropped

\- .gitignore matches literal filenames on disk, not what an editor buffer thinks it saved



\*\*Next:\*\*

\- Days 3-4: first direct Bedrock call, set up AWS Budget alarm before making it



\---

