import os


def common_middleware(args):
    input_file = args.file
    prompt = args.prompt
    openai_api_key = args.key or os.environ.get("OPENAI_API_KEY", None)
    temperature = args.temperature

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
