import os
import time
import argparse

from typing import *
from rich import print
from groq import Groq

from .prompts import LATEX_PROMPT


MAX_PROMPT_LENGTH = 500 # characters
DEFAULT_MODEL = "llama3-70b-8192"
AVAILABLE_MODEL_NAMES = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "gemma2-9b-it",
]


def create_llm_client() -> Groq:
    try:
        llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        return llm
    except Exception as e:
        print(f">> [bold red]ClientError: cannot create the LLM client.[/]")
        exit(1)


def get_latex_response(
        llm: Groq,
        user_input: str,
        model_name: Optional[str] = DEFAULT_MODEL
    ) -> str:
    if model_name not in AVAILABLE_MODEL_NAMES:
        print(f">> [bold red]ModelError: the model name {model_name} is not available.[/]")
        exit(1)
    
    prompt = LATEX_PROMPT.format(user_input=user_input)
    messages = [dict(role="user", content=prompt)]

    chat_completion = llm.chat.completions.create(
        messages=messages,
        model=model_name,
    )

    output = chat_completion.choices[0].message.content.strip()
    if not output.startswith("latex:"):
        print(f">> [bold red]OutputError: invalid output encountered, try again.[/]")
        exit(1)

    output = output.replace("latex:", "").strip()
    return output


def create_parser():
    parser = argparse.ArgumentParser(description="smoltex: from natural language descriptions to latex equations.")
    
    # required args
    parser.add_argument("prompt", type=str, help="input prompt (max 500 characters)")
    
    # optional args
    parser.add_argument("-m", "--model_name", type=str, choices=AVAILABLE_MODEL_NAMES, help="name of the model to use (optional)")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    prompt = args.prompt.strip()
    model_name = args.model_name

    if len(prompt) > MAX_PROMPT_LENGTH:
        print(">>[bold red]ArgumentError: prompt must not exceed 500 characters.[/]")
        exit(1)

    llm = create_llm_client()

    start = time.time()
    output = get_latex_response(llm, prompt, model_name=model_name or DEFAULT_MODEL)
    end = time.time()

    print(f"\n[bold green]Latex string:[/] {output}")
    print(f"\n>> completion time: [bold yellow]{(end - start)*1000} ms[/]")
    print()


if __name__ == "__main__":
    main
