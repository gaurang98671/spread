import argparse
from middleware import add_common_arguments

from controllers import spread_controller, compare_controller

parser = argparse.ArgumentParser(
    description="A simple command-line tool to test quality of LLM prompts"
)

subpraser = parser.add_subparsers(
    title="Check spread of LLM outputs for input prompt",
    dest="sub_command",
    required=True,
)

# Spread
spread_parser = subpraser.add_parser("spread", help="Checks the Spread of LLM Outputs")
spread_parser = add_common_arguments(spread_parser)

# Compare
compare_parser = subpraser.add_parser("compare", help="Gives the average distance between prompt and target output")
compare_parser = add_common_arguments(compare_parser)
compare_parser.add_argument(
    "--target",
    help="Target prompt output. This could be passed in as a string or a text file",
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
