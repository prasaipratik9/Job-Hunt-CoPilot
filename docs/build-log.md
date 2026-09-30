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



\---------------------------------------------------------------------------------------------------------------------------



\## \[2026-09-28] - Day 5



\*\*Shipped:\*\*

\- Wrote extract\_requirements.py, Stage 1 of the pipeline: pasted job posting in, list of requirements tagged must-have or nice-to-have out

\- Prompt iterated from 16 noisy items (job title, perks, location included) to clean, specific, source-traceable lists

\- Switched extraction model from Nova Micro to Nova Lite, which follows multi-rule prompts more reliably

\- Tested on two very different postings (AI/MCP role and graduate program) plus their Employer questions sections



\*\*Stuck / broke:\*\*

\- Adding Employer questions rules made Micro drop the whole posting body

\- Example in my own prompt (AWS DevOps) leaked into the output for a posting that never mentioned it

\- Stricter prompt then dropped some questionnaire skills (TDD, MVC), accepted for v1



\*\*Learned:\*\*

\- Small models need concrete examples in the prompt, and a bigger model can fix what wording tweaks cannot

\- Examples in a prompt can be copied into the output, so use throwaway examples and forbid invented items

\- Every prompt change needs a retest on earlier postings, since fixing one part can break another

\- Never trust model output: Model output is validated before use (code fences stripped, JSON checked, bad tags defaulted- Each function does one job (load, call, parse, orchestrate), which lets later stages import extract\_requirements()

\- Temperature 0.0 gives near-identical output on the same input, so prompt changes stay comparable

\- Check every extracted item against the source posting yourself



\---------------------------------------------------------------------------------------------------------------------------



\## \[2026-09-29] - Day 6



\*\*Shipped:\*\*

\- Wrote match\_resume.py, Stage 2 of the pipeline: embeds resume chunks and requirements via Titan Text Embeddings V2, scores every pair with cosine similarity, keeps the top 2 matching chunks per requirement

\- Ran it end-to-end on job\_posting\_1.txt: scores correctly separated real resume content (Python/TypeScript 0.39, JavaScript 0.39, API integration 0.24) from content with no resume support (Aged Care Empathy 0.07)



\*\*Learned:\*\*

\- An embedding is a fixed-length array of floats regardless of input length, the model sets the length (dimensions), not the input

\- Cosine similarity never sees the actual words, it only compares two number arrays geometrically; low score = wide angle = no overlapping meaning in the embedding space

\- Explained why Aged Care Empathy scored lowest: no resume content shares meaning with it, so the vectors point in very different directions

\- A skill-dense chunk (TECHNICAL SKILLS) wins most requirement matches by default since it's packed with content, worth splitting further in polish days for sharper matches

\- Low absolute scores (under 0.4) are normal here, the relative gap between requirements matters more than the raw number

\- Still to properly learn: the invoke\_model request/response shape (dimensions, normalize, parsing the body) that embed\_text() actually uses



\*\*Next:\*\*

\- Stage 3: score\_fit(), turn these match scores into a single 0-100 fit percentage, weighted toward must-have requirements



\---



