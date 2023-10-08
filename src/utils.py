import numpy as np
import miniball
import openai
from scipy.spatial import distance


def get_distance(p1, p2):
    if len(p1) != len(p2):
        raise (Exception(f"Incorrect dimensions p1: {len(p1)} p2: {len(p2)}"))

    dist = []
    for i in range(len(p1)):
        dist.append((p1[i] - p2[i]) ** 2)
    return sum(dist) / len(dist)


def get_similarity_score(points):
    center = get_center(points)
    distance = [get_distance(center, x) for x in points]
    score = (sum(distance) / len(distance)) * 10**4
    return round(score, 3)


def get_center(points):
    points = np.array(points)
    distances = distance.cdist(points, points, "euclidean")
    center_index = np.argmin(distances.sum(axis=0))
    center = points[center_index]
    return center


def generate_vector(data, engine="text-embedding-ada-002"):
    response = openai.Embedding.create(input=data, model=engine)
    return response["data"][0]["embedding"]


def call_open_ai(prompt, engine, temperature, calls, openai_api_key):
    openai.api_key = openai_api_key
    outputs = []

    for i in range(int(calls)):
        print(f"Calling OpenAI({i+1}/{calls})", end="\r")
        response = openai.Completion.create(
            engine=engine, temperature=temperature, prompt=prompt, max_tokens=500
        )

        response_text = response["choices"][0]["text"]

        embeddings = generate_vector(data=response_text)
        outputs.append(tuple(embeddings))
    print("")

    return outputs, response_text


def bold(text):
    bold_text = "\033[1m"
    reset_text = "\033[0m"
    return bold_text + text + reset_text
