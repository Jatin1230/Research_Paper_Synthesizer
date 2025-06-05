# agents/paper_agent.py
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq  # or use OpenAI/Gemini if preferred
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    api_key=os.getenv("GROQ_API_KEY")
)

def summarize_papers(papers: list):
    input_text = "\n\n".join(
        [f"Title: {p['title']}\nSummary: {p['summary']}" for p in papers]
    )

    prompt = PromptTemplate.from_template("""
Compare the following research papers in terms of:
1. Core Method/Approach
2. Results/Accuracy (use numeric values if available, e.g., accuracy %, F1, etc.)
3. Limitations

Return structured bullet points like:
- Paper A: Method ..., Accuracy: 91.2%, Limitation: ...
- Paper B: ...
{paper_summaries}
""")


    chain = prompt | llm
    result = chain.invoke({"paper_summaries": input_text})
    return result.content
