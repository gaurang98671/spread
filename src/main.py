import argparse
from controllers import spread_controller, compare_controller

parser = argparse.ArgumentParser(
    description="A simple command-line tool to test quality of LLM prompts"
)

subpraser = parser.add_subparsers(
    title="Check spread of LLM outputs for input prompt",
    dest="sub_command",
    required=True,
)

# Add common arguments
parser.add_argument("-f", "--file", help="Prompt text file")
parser.add_argument("-n", "--calls", default=10, help="Number of calls to LLM")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument("--key", help="OpenAI key")
parser.add_argument("-p", "--prompt", help="Prompt")
parser.add_argument("--temperature", default=0, help="LLM temperature")
parser.add_argument("--engine", default="text-davinci-003")
parser.add_argument("--log", help="Create a log file for all prompt outputs")

# Add subcommands
# Spread
spread_parser = subpraser.add_parser("spread")

# Compare
compare_parser = subpraser.add_parser("compare")
compare_parser.add_argument(
    "-target",
    required=True,
    help="Target prompt output. This could be passed in as string or a text file",
)

# Parse the command-line arguments
args = parser.parse_args()
subcommand = args.sub_command
verbose = args.verbose
log_suffix = args.log

if verbose:
    print(args)

# Access the parsed arguments
if subcommand == "spread":
    spread_controller(args=args)
elif subcommand == "compare":
    compare_controller(args=args)
