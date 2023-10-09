import argparse
import os
from middleware import common_middleware
from utils import call_open_ai, get_center, get_similarity_score, bold

parser = argparse.ArgumentParser(
    description="A simple command-line tool to test quality of LLM prompts"
)

subpraser = parser.add_subparsers(
    title="Check spread of LLM outputs for input prompt", dest="sub_command", required=True
)

# Add common arguments
parser.add_argument("-f", "--file", help="Prompt text file")
parser.add_argument("-n", "--calls", default=10, help="Number of calls to LLM")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument("--key", help="OpenAI key")
parser.add_argument("-p", "--prompt", help="Prompt")
parser.add_argument("--temperature", default=0, help="LLM temperature")
parser.add_argument("--engine", default="text-davinci-002")
parser.add_argument("--log", help="Create a log file for all prompt outputs")

# Add subcommands
spread_parser = subpraser.add_parser("spread")
compare_parser = subpraser.add_parser("compare")


# Parse the command-line arguments
args = parser.parse_args()
subcommand = args.sub_command
verbose = args.verbose
log_suffix = args.log

if verbose:
    print(args)

# Access the parsed arguments
if subcommand == "spread":
    err = common_middleware(args=args)
    if err == None:
        call_embeddings, response_text = call_open_ai(
            args.prompt,
            engine=args.engine,
            temperature=float(args.temperature),
            calls=int(args.calls),
            openai_api_key=args.key,
            log_suffix=log_suffix,
            verbose=verbose)
        score = get_similarity_score(call_embeddings)
        print(f"{bold('Spread')}: {score}")
    else:
        print(err)
