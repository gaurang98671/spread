from utils import (
    call_open_ai,
    get_similarity_score,
    bold,
    generate_vector,
    get_distance,
)
import copy


def handle_command(args, controller, middlewares):
    
    # Handle all middlewares
    for middleware in middlewares:
        err = middleware(args=args)
        if err != None:
            print(err)

    # Run controller for each prompt
    prompts = args.prompt
    for prompt in prompts:
        args_copy = copy.deepcopy(args)
        args_copy.prompt = prompt
        controller(args_copy)


def spread_controller(args):
    call_embeddings, _, err = call_open_ai(
        args.prompt,
        engine=args.engine,
        temperature=float(args.temperature),
        calls=int(args.calls),
        openai_api_key=args.key,
        log_prefix=args.log,
        verbose=args.verbose,
    )

    if err != None:
        print(err)
    else:
        score = get_similarity_score(call_embeddings)
        print(f"{bold('Spread')}: {score}")


def compare_controller(args):
    target_embeddings = generate_vector(args.target)
    call_embeddings, _, err = call_open_ai(
        args.prompt,
        engine=args.engine,
        temperature=float(args.temperature),
        calls=int(args.calls),
        openai_api_key=args.key,
        log_prefix=args.log,
        verbose=args.verbose,
    )

    if err != None:
        print(err)
    else:
        avg_distance = sum(
            [get_distance(target_embeddings, x) for x in call_embeddings]
        ) / len(call_embeddings)
        print(f"{bold('Distance')} : {avg_distance}")
