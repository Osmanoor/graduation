# graduation
## 1. prompt used for creating the papers summeries 

Act as a research assistant. Provide a concise technical overview of the attached paper using these exact headings:
Short Description: A 2-sentence overview of the paper’s goal.
Research Question: The specific problem the authors aim to solve.
Main Methodology: The primary technical approach or framework proposed.
Dataset & Benchmark: The specific datasets and evaluation metrics used.
Research Contributions: In no more than two paragraphs, identify the novelty of this work, the specific technical gaps it fills, and the most significant findings or improvements it offers to the field.

2.prompt used for creating the gemini chat summeries

As you know, I am working on my graduation research project regarding Improving Recall in Arabic RAG Systems using Query Enhancement. I am currently consolidating my research across different AI sessions to build a "Live Research Log" in my repository.
I need you to review our entire conversation history in this specific chat and generate a comprehensive Session Archive Report in Markdown format.
Unlike a brief summary, I want this to be comprehensive. Do not filter out "minor" points if they were relevant to the research process. I need to capture the full breadth of our discussion.
Please format the response strictly as a Markdown code block structure (.md) as follows:
🗂️ Session Archive: [Insert Main Topic of this Chat]
1. 🧠 Chat Persona & Perspective
In this session, what "role" or "mindset" did you adopt? (e.g., Did you act as a Dataset Critic? A Python Engineer? An Academic Reviewer?)
What was your primary stance or bias regarding the project direction? (e.g., "Advocated strongly for specialized query datasets over general corpora.")
2. 🗣️ Comprehensive Discussion Log
List all significant topics, concepts, and ideas we discussed. Do not limit this to just the final decisions; include the brainstorming process.
Topic A: [Detail what was discussed]
Topic B: [Detail what was discussed]
Topic C: [Detail what was discussed]
(Continue for all topics covered)
3. 💡 Insights & realizations
List the insights gathered during our discussion. These can be theoretical, practical, or strategic.
Insight 1...
Insight 2...
4. ✅ Recommendations & Justifications (Methodology Support)
List every recommendation you made, along with the academic or technical justification (The "Why"). This is crucial for writing my thesis Methodology chapter.
Recommendation	Category (Dataset/Algo/Scope)	Justification & Rationale	Trade-offs Discussed
[e.g., Use TyDi QA]	[Dataset]	[Why this fits Arabic morphology...]	[What we lose by choosing this...]
[Item 2]	...	...	...
[Item 3]	...	...	...
5. ⚠️ Identified Risks & Challenges
What warnings or potential roadblocks did we discuss? (e.g., Lack of dialect data, computational costs, evaluation difficulty).
Instruction: Base this report strictly on our conversation history. Do not generate new advice now; I want to document exactly what we have already brainstormed and decided in this session.