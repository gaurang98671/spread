import os
from argparse import Namespace, ArgumentParser
from typing import Optional

def common_middleware(args: Namespace) -> Optional[str]:
    input_file = args.file
    prompt = args.prompt
    np = args.nprompt

    # Handle prompt
    if prompt is None and input_file is None and np is None:
        return "No input file or prompt was provided"
    elif np != None:
        files = np.split(",")
        prompts = []
        for file_name in files:
            prompt_file = open(file_name, "r")
            prompts.append(prompt_file.read())
            prompt_file.close()
        args.prompt = prompts

    elif input_file is not None:
        prompt_file = open(input_file, "r")
        args.prompt = [prompt_file.read()]
        prompt_file.close()
    else:
        args.prompt = [args.prompt]

    # Check OPENAI_API_KEY
    openai_api_key = args.key or os.environ.get("OPENAI_API_KEY", None)
    if openai_api_key == None:
        return "No open AI API key found \nAdd the OPEN_AI_KEY in enviromnent variables or pass it with --key flag"
    else:
        args.key = openai_api_key

    return None


def compare_middleware(args: Namespace) -> None:
    target = args.target

    if target.endswith(".txt"):
        if args.verbose:
            print(f"Parsing {target} file")
        try:
            f = open(target, "r")
            args.target = f.read()
            f.close()
        except FileExistsError as e:
            raise Exception(f"{target} file not found")


def add_common_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument("-f", "--file", help="Prompt text file")
    parser.add_argument("-n", "--calls", default=10, help="Number of calls to LLM")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--key", help="OpenAI key")
    parser.add_argument("-p", "--prompt", help="Prompt")
    parser.add_argument(
        "-np", "--nprompt", help="Multiple prompts as comma seperated list"
    )
    parser.add_argument("--temperature", default=0, help="LLM temperature")
    parser.add_argument("--engine", default="text-davinci-003")
    parser.add_argument("--log", help="Create a log file for all prompt outputs")

    return parser
