from utils import (
    get_spread,
    bold,
    read_yaml,
    print_color,
    get_responses_embeddings_and_avg_time_per_call,
    get_avg_embeddings_distance,
    get_jaro_similarity
)
from copy import deepcopy
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
            args_copy = deepcopy(args)
            args_copy.prompt = prompt
            controller(args_copy)
    else:
        controller(args)


def spread_controller(args: Namespace) -> None:
    _, call_embeddings, _ = get_responses_embeddings_and_avg_time_per_call(args=args)
    score = get_spread(call_embeddings)
    print(f"{bold('Spread')}: {score}")


def compare_controller(args: Namespace) -> None:
    responses, call_embeddings, _ = get_responses_embeddings_and_avg_time_per_call(args=args)

    counter = 1
    avg_similarity = 0
    for response in responses:
        similarity = get_jaro_similarity(response, args.target)
        print(f"Response {counter}: {similarity}")
        avg_similarity += similarity / len(responses)
        counter += 1
    print(f"{bold('Average similarity')} : {avg_similarity}")


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