from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def stateless_chatbot(prompts: str) -> str:
    
    client = OpenAI()
    response = client.responses.create(
        model = os.getenv("LLM_MODEL"),
        input = prompts
    )

    print(response.output_text)

stateless_chatbot("Who is the PM of the UK?")
stateless_chatbot("Who was before him?")