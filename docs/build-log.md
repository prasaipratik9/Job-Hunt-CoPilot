\# Job Hunt Copilot — Build Log



\## \[2026-09-27] — Days 1-2



\*\*Shipped:\*\*

\- Wrote and ran resume\_chunker.py, splits resume into structured chunks (id, text, length)

\- Verified output against real resume, tuned chunking by adding blank lines to SUMMARY

\- Created GitHub repo (public), with README and Python .gitignore



\*\*Learned:\*\*

\- with open() as a context manager for safe file reading

\- String splitting on blank lines to chunk text, plus filtering short chunks by length

\- id in chunk dicts comes from the original unfiltered index, can skip numbers if a chunk is dropped

\- .gitignore matches literal filenames on disk, not what an editor buffer thinks it saved



\---------------------------------------------------------------------------------------------------------------------------



\## \[2026-09-28] - Days 3-4



\*\*Shipped:\*\*

\- Created a $10 monthly AWS Budget alarm before making any Bedrock call

\- Wrote and ran bedrock\_first\_call.py: first direct Bedrock call using the Converse API with Nova Micro (us-east-1), authenticated with a short-lived Bedrock API key held in an environment variable

\- First call returned in 820ms using 27 input and 60 output tokens



\*\*Learned:\*\*

\- Converse response shape: reply text lives at output > message > content\[0] > text, and usage/stopReason sit alongside it

\- Lower temperature (0.2) gives predictable output, suited to extraction and scoring; higher suits drafting

\- Use python -m pip when pip isn't on PATH

\- Bedrock is the model service; AgentCore is a separate agent-hosting service not needed for this project



\*\*Next:\*\*

\- Days 5-7: staged pipeline, starting with extract\_requirements() on a pasted job posting



\---





