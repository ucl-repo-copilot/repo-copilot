import asyncio
import os
from typing import Optional, Sequence, Any, List, Dict
from llama_index.core.evaluation import RelevancyEvaluator, CorrectnessEvaluator , AnswerRelevancyEvaluator
from llama_index.llms.azure_openai import AzureOpenAI
from repo_documentation.prompt import DOCUMENTATION_PROMPT
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

llm = AzureOpenAI(
    engine="GPT-4", model="gpt-4", temperature=0.0, 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("BASE_URL"), 
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

async def evaluate_answer_relevancy(query: str, response: str):  
    evaluator = AnswerRelevancyEvaluator(llm=llm)
    eval_result = await evaluator.aevaluate(query=query, response=response)
    return eval_result

async def evaluate_relevancy(query: str, response: str, file_content: str):
   
    evaluator = RelevancyEvaluator(llm=llm)
    eval_result = await evaluator.aevaluate(query=query, response=response, contexts=[file_content])
    return eval_result
