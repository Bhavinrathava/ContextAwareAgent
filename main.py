import os 
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from typing import List

class CommaSeparatedListOutputParser(BaseOutputParser[List[str]]):
    """Parse the output of an LLM call to a comma-separated list."""


    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""
        return text.strip().split(", ")
    

def main():
    openAIKey = 'OPENAI_KEY'
    key = os.environ.get(openAIKey)
    print(f"Testing Environment Variable: {key}")

    template = """You are a helpful assistant who generates comma separated lists.
    A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
    ONLY return a comma separated list, and nothing more."""
    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template),
        ("human", human_template),
    ])
    chain = chat_prompt | ChatOpenAI(openai_api_key=key) | CommaSeparatedListOutputParser()
    print(chain.invoke({"text": "colors"}))

if __name__ == "__main__":
    print("Running main")
    main()