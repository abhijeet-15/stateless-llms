# Stateless LLM Routing & Multi-Provider Architecture

A lightweight, production-ready pattern for routing requests dynamically across multiple LLM providers (**OpenAI**, **Groq**, and **OpenRouter**) using environment-driven configuration and standard OpenAI-compatible endpoints.

---

## Key Architectural Concepts

### 1. The Stateless Nature of LLMs (*Message In, Message Out*)
LLMs have **no inherent memory or internal state**. Every API request is evaluated in an isolated vacuum. The model retains no knowledge of previous prompts, earlier turns, or its own generated answers.

### 2. Simulating State via Context Injection
Because LLMs cannot retain history, "memory" is simulated by transmitting the full cumulative conversation thread in the `messages` payload on each round-trip:

```python
messages = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What is their GDP?"}
]
```

Without the preceding turns, the model cannot resolve the pronoun **"their"**. By appending both user inputs and assistant replies sequentially, the context window provides the requisite reference data for multi-turn coherence.

---

## Supported Providers

| Provider | Role in Stack | Primary Advantage |
| :--- | :--- | :--- |
| **OpenAI** | Industry Benchmark | High reasoning capability, structured outputs, direct native standard. |
| **Groq** | Low-Latency Inference | LPU-powered throughput for rapid response generation. |
| **OpenRouter** | Multi-Model Gateway | Single endpoint aggregating proprietary and open-weights models (including free tiers). |

---

## System Design & Routing Logic

1. **Decoupled Configuration**: All provider credentials, model names, and base URLs reside strictly in `.env` without hardcoded constants.
2. **Provider Schema**: A frozen `@dataclass` acts as an immutable configuration schema:
   ```python
   @dataclass(frozen=True)
   class Provider:
       name: str
       env_var: str
       is_free: bool
       base_url: str | None
       model: str
   ```
3. **OpenAI Compatibility**: All integrated providers adhere to the OpenAI API specification, allowing a single `OpenAI` client instance to switch endpoints seamlessly via `base_url`.
4. **Dynamic Resolution**: Provider priority is resolved at runtime based on active keys in the environment.

---

## Environment Setup

Create a `.env` file in the project root:

```env
# OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=
OPENAI_LLM_MODEL=gpt-4o-mini

# Groq
GROQ_API_KEY=your_groq_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_LLM_MODEL=llama-3.1-8b-instant

# OpenRouter
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_LLM_MODEL=openrouter/free
```

## Quickstart

Run via `uv`:

```bash
uv run provider.py
```