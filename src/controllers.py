from utils import (
    call_open_ai,
    get_similarity_score,
    bold,
    generate_vector,
    get_distance,
)
from middleware import common_middleware, compare_middleware


def spread_controller(args):
    err = common_middleware(args=args)
    if err == None:
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
    else:
        print(err)


def compare_controller(args):
    err = common_middleware(args=args)
    err2 = compare_middleware(args)

    if err != None:
        print(err)
    elif err2 != None:
        print(err2)
    else:
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
