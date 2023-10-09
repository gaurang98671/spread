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


# TODO: To be implemented
def compare_middleware(args):
    pass
