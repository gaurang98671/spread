from utils import (
    call_open_ai,
    get_similarity_score,
    bold,
    generate_vector,
    get_distance,
    read_yaml,
    print_color,
    get_responses_embeddings_and_avg_time_per_call,
    get_avg_embeddings_distance,
)
import copy
from TestCase import TestCase
import sys
from argparse import Namespace
from typing import Callable, List

def handle_command(args: Namespace, controller: Callable[..., None], middlewares: List[Callable[..., None]]):
    # Handle all middlewares
    for middleware in middlewares:
        err = middleware(args=args)
        if err != None:
            print(err)

    # Run controller for each prompt
    if "prompt" in args:
        prompts = args.prompt
        for prompt in prompts:
            args_copy = copy.deepcopy(args)
            args_copy.prompt = prompt
            controller(args_copy)
    else:
        controller(args)


def spread_controller(args: Namespace) -> None:
    _, call_embeddings, _ = get_responses_embeddings_and_avg_time_per_call(args=args)
    score = get_similarity_score(call_embeddings)
    print(f"{bold('Spread')}: {score}")


def compare_controller(args: Namespace) -> None:
    _, call_embeddings, _ = get_responses_embeddings_and_avg_time_per_call(args=args)
    avg_distance = get_avg_embeddings_distance(call_embeddings, args.target)
    print(f"{bold('Distance')} : {avg_distance}")


def test_controller(args: Namespace) -> None:
    test_config_data = read_yaml(args.file)
    failed_count = 0
    for index, section in enumerate(test_config_data):
        print_color("BOLD", section)
        print("-" * 50)
        for prompts in test_config_data.get(section, []):
            for sub_prompt in prompts["prompts"]:
                p = TestCase(sub_prompt)
                status, failures = p.run_test_case()
                failed_count += failures
        if index < len(test_config_data) - 1:
            print("")

    if failed_count > 0:
        print_color("FAIL", f"Total failures : {failed_count}")
        sys.exit(1)
    

