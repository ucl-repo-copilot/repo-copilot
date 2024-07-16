import asyncio
import os
from typing import Optional, Sequence, Any, List, Dict
from llama_index.core.evaluation import RelevancyEvaluator, EvaluationResult
from llama_index.llms.azure_openai import AzureOpenAI
from repo_documentation.prompt import DOCUMENTATION_PROMPT
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

async def evaluate_documentation(query: str, response: str, file_content: str):
    llm = AzureOpenAI(
        engine="GPT-4", model="gpt-4", temperature=0.0, 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("BASE_URL"), 
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
    evaluator = RelevancyEvaluator(llm=llm)
    eval_result = await evaluator.aevaluate(query=query, response=response, contexts=[file_content])
    return eval_result
