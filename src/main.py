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

# Subcommands

# Spread
spread_parser = subpraser.add_parser("spread")
spread_parser = add_common_arguments(spread_parser)

# Compare
compare_parser = subpraser.add_parser("compare")
compare_parser = add_common_arguments(compare_parser)
compare_parser.add_argument(
    "--target",
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
