import os


def common_middleware(args):
    input_file = args.file
    prompt = args.prompt
    openai_api_key = args.key or os.environ.get("OPENAI_API_KEY", None)

    if prompt is None and input_file is None:
        return "No input file or prompt was provided"

    elif input_file is not None:
        prompt_file = open(input_file, "r")
        args.prompt = prompt_file.read()
        prompt_file.close()

    # Preprocess arguments
    if openai_api_key == None:
        return "No open AI API key found \nAdd the OPEN_AI_KEY in enviromnent variables or pass it with --key flag"
    else:
        args.key = openai_api_key

    return None


def compare_middleware(args):
    
    target = args.target

    if target.endswith(".txt"):

        if args.verbose:
            print(f"Parsing {target} file")
        try:
            f = open(target, "r")
            args.target = f.read()
            f.close()
        except FileExistsError as e:
            return f"{target} file not found"
        
def add_common_arguments(parser):
    parser.add_argument("-f", "--file", help="Prompt text file")
    parser.add_argument("-n", "--calls", default=10, help="Number of calls to LLM")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--key", help="OpenAI key")
    parser.add_argument("-p", "--prompt", help="Prompt")
    parser.add_argument("-np", "--nprompt", help="Multiple prompts as comma seperated list")
    parser.add_argument("--temperature", default=0, help="LLM temperature")
    parser.add_argument("--engine", default="text-davinci-003")
    parser.add_argument("--log", help="Create a log file for all prompt outputs")

    return parser
