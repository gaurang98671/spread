import numpy as np
import openai
from scipy.spatial import distance
import os
import yaml
import json
import time


def get_distance(p1, p2):
    if len(p1) != len(p2):
        raise (Exception(f"Incorrect dimensions p1: {len(p1)} p2: {len(p2)}"))

    dist = []
    for i in range(len(p1)):
        dist.append((p1[i] - p2[i]) ** 2)
    return sum(dist) / len(dist)


def get_similarity_score(points, precesion=3):
    center = get_center(points)
    distance = [get_distance(center, x) for x in points]
    score = (sum(distance) / len(distance)) * 10**4
    return round(score, precesion)


def get_center(points):
    points = np.array(points)
    distances = distance.cdist(points, points, "euclidean")
    center_index = np.argmin(distances.sum(axis=0))
    center = points[center_index]
    return center


def get_avg_embeddings_distance(embeddings, target_text):
    target_embeddings = generate_vector(target_text)
    return sum([get_distance(target_embeddings, x) for x in embeddings]) / len(
        embeddings
    )


def generate_vector(data, engine="text-embedding-ada-002"):
    response = openai.Embedding.create(input=data, model=engine)
    return response["data"][0]["embedding"]


# TODO : Add support for chat complemetion models like gpt-3.5-turbo
def call_open_ai(
    prompt, engine, temperature, calls, openai_api_key, log_prefix=None, verbose=False
):
    openai.api_key = openai_api_key
    outputs = []
    time_per_call_in_seconds = []

    for i in range(int(calls)):
        if verbose:
            print(f"Calling OpenAI({i+1}/{calls})", end="\r")

        try:
            start_time = time.time()
            response = openai.Completion.create(
                engine=engine, temperature=temperature, prompt=prompt
            )
            end_time = time.time()
            time_per_call_in_seconds.append(end_time - start_time)
            response_text = response["choices"][0]["text"].replace("\n", "")
        except Exception as e:
            raise (Exception("Failed to called openai. Check log for err messagee"))

        # Store logs
        if log_prefix:
            create_directory_if_not_exists("logs", verbose=verbose)
            log_file = open(f"logs/{log_prefix}.log", "a")
            log_file.write(f"\nOpenAI response : {response_text}")
            log_file.close()

        embeddings = generate_vector(data=response_text)
        outputs.append(tuple(embeddings))
    print("")

    return (
        outputs,
        response_text,
        sum(time_per_call_in_seconds) / len(time_per_call_in_seconds),
    )


def bold(text):
    bold_text = "\033[1m"
    reset_text = "\033[0m"
    return bold_text + text + reset_text


def print_color(color, text):
    colors = {
        "HEADER": "\033[95m",
        "OKBLUE": "\033[94m",
        "OKCYAN": "\033[96m",
        "OKGREEN": "\033[92m",
        "WARNING": "\033[93m",
        "FAIL": "\033[91m",
        "ENDC": "\033[0m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
    }

    print(f"{colors.get(color)}{text}{colors.get('ENDC')}")


def create_directory_if_not_exists(directory_name, verbose=False):
    if not os.path.exists(directory_name):
        try:
            # Create the directory
            os.makedirs(directory_name)
            if verbose:
                print(f"Directory '{directory_name}' created.")
        except OSError as e:
            if verbose:
                print(f"Error creating directory '{directory_name}': {str(e)}")


def read_yaml(file_name):
    file = open(file_name, "r")
    yaml_text = file.read()
    file.close()
    yaml_dict = yaml.safe_load(yaml_text)
    return yaml_dict


def read_json(file_name):
    file = open(file_name, "r")
    json_text = file.read()
    file.close()
    json_dict = json.loads(json_text)
    return json_dict


def get_embeddings(args=None, dict=None):
    if args:
        call_embeddings, _, avg_time_per_call = call_open_ai(
            args.prompt,
            engine=args.engine,
            temperature=float(args.temperature),
            calls=int(args.calls),
            openai_api_key=args.key,
            log_prefix=args.log,
            verbose=args.verbose,
        )
    elif dict:
        call_embeddings, _, avg_time_per_call = call_open_ai(
            dict.get("prompt"),
            engine=dict.get("engine"),
            temperature=float(dict.get("temperature")),
            calls=int(dict.get("calls")),
            openai_api_key=dict.get("key"),
        )

    return call_embeddings, avg_time_per_call
