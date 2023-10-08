import argparse
import os
from middleware import spread_middleware
from utils import call_open_ai, get_center, get_similarity_score, bold

parser = argparse.ArgumentParser(
    description="A simple command-line tool to test quality of LLM prompts"
)

subpraser = parser.add_subparsers(
    title="Check spread of LLM outputs for input prompt", dest="sub_command"
)

spread_parser = subpraser.add_parser("spread")
spread_parser.add_argument("-f", "--file", help="Prompt text file")
spread_parser.add_argument("-n", "--calls", default=10, help="Number of calls to LLM")
spread_parser.add_argument("--key", help="OpenAI key")
spread_parser.add_argument("-p", "--prompt", help="Prompt")
spread_parser.add_argument("--temperature", default=0, help="LLM temperature")
spread_parser.add_argument("--engine", default="text-davinci-002")

# Parse the command-line arguments
args = parser.parse_args()
subcommand = args.sub_command

# Access the parsed arguments
if subcommand == "spread":
    err = spread_middleware(args=args)
    if err == None:
        call_embeddings, response_text = call_open_ai(args.prompt, engine=args.engine, temperature=float(args.temperature), calls=int(args.calls), openai_api_key=args.key)
        score = get_similarity_score(call_embeddings)
        print(f"{bold('Score')}: {score}")
    else:
        print(err)
