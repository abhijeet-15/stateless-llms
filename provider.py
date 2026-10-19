import os
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass(frozen=True)
class Provider:
    """
    One provider to route all requests reliably across all inference providers
    """
    name: str
    env_var: str
    is_free: bool
    base_url: str|None
    model: str

PROVIDERS= [
    Provider("OpenAI", "OPENAI_API_KEY", False, "OPENAI_BASE_URL", "OPENAI_LLM_MODEL"),
    Provider("Groq","GROQ_API_KEY",True,"GROQ_BASE_URL","GROQ_LLM_MODEL"),
    Provider("OpenRouter", "OPENROUTER_API_KEY",True,"OPENROUTER_BASE_URL","OPENROUTER_LLM_MODEL"),

]


def select_provider() -> Provider:
    for provider in PROVIDERS:
        if os.getenv(provider.env_var):
            return provider
    expected = ", ".join(p.env_var for p in PROVIDERS)
    raise RuntimeError(f"No provider key set, add one of {expected} to your environment variables")


def build_client(provider: Provider) -> OpenAI:
    api_key = os.getenv(provider.env_var)
    base_url = os.getenv(provider.base_url) if provider.base_url else None
    print(f"base url: {base_url}")
    return OpenAI(
        api_key = api_key,
        base_url = base_url,
    )



def have_any_key() -> bool:
    return any(os.getenv(p.env_var) for p in PROVIDERS )

print("Found a provider key." if have_any_key() else "No provider key found!")

def llm_reply(prompt: str) -> str:
    provider = select_provider()
    print(f" api key : {os.getenv(provider.env_var)}")
    client = build_client(provider)
    result = client.chat.completions.create(
        model = os.getenv(provider.model) if provider.model else None,
        max_completion_tokens = 2048,
        messages = [
            {
                "role" : "user",
                "content" : prompt

            }
        ]
    )
    
    return result.choices[0].message.content

prompt = "Who holds the record for maximum number of centuries in ODI cricket"

try:
    print(llm_reply(prompt))
except Exception as e:
    print(f"Error: {e}")