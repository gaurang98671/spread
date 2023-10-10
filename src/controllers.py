from utils import call_open_ai, get_center, get_similarity_score, bold
from middleware import common_middleware

def spread_controller(args):
    err = common_middleware(args=args)
    if err == None:
        call_embeddings, response_text = call_open_ai(
            args.prompt,
            engine=args.engine,
            temperature=float(args.temperature),
            calls=int(args.calls),
            openai_api_key=args.key,
            log_prefix=args.log,
            verbose=args.verbose)
        score = get_similarity_score(call_embeddings)
        print(f"{bold('Spread')}: {score}")
    else:
        print(err)
