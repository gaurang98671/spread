from utils import (
    read_json,
    print_color,
    get_embeddings,
    get_avg_embeddings_distance,
    get_similarity_score,
)
import os
from argparse import Namespace


class TestCase:
    def __init__(self, prompt: dict) -> None:
        self.__check_prompt(prompt)

        self.name = prompt.get("name")
        self.prompt = self.__set_prompt(prompt)
        self.mocks = self.__set_mocks(prompt)
        self.calls = prompt.get("calls", 1)
        self.engine = prompt.get("engine", "text-davinci-003")
        self.temperature = prompt.get("temperature", 0.0)
        self.key = self._set_api_key(prompt)

        # Set criteria
        self.time = prompt.get("time", None)
        self.target = self._set_target(prompt) if "target" in prompt else None
        self.spread = prompt.get("spread", None)

    def run_test_case(self):
        failure_stats = []

        if self.time == None and self.target == None and self.spread == None:
            print_color("WARNING", "No test criteria were found")
            return {}, 0
        
        if len(self.mocks) > 0:
            for mock_file, mock_data in self.mocks.items():
                print(f"For {mock_file}")
                args = {
                    "prompt": self.prompt.format(**mock_data),
                    "engine": self.engine,
                    "temperature": self.temperature,
                    "calls": self.calls,
                    "key": self.key,
                }
                failure_stats.append(self.display_results(args))
                print("")
        else:
            # Just run for prompt if no mock data is found
            args = {
                "prompt": self.prompt,
                "engine": self.engine,
                "temperature": self.temperature,
                "calls": self.calls,
                "key": self.key,
            }
            failure_stats.append(self.display_results(args))

        return failure_stats, sum([len(x) for x in failure_stats])


    def display_results(self, args: Namespace):
        embeddings, avg_time_per_call = get_embeddings(dict=args)
        failure_stats = {}

        if self.spread is not None:
            spread = get_similarity_score(embeddings, 8)
            print("SPREAD : ", end="")
            if spread < self.spread:
                print_color("OKGREEN", "PASSED")
            else:
                print_color("FAIL", "FAILED")
                failure_stats.update({"spread": spread})

        if self.target is not None:
            distance = get_avg_embeddings_distance(embeddings, self.target.get("text"))
            print("TARGET : ", end="")
            if distance < self.target.get("max"):
                print_color("OKGREEN", "PASSED")
            else:
                print_color("FAIL", "FAILED")
                failure_stats.update({"target":distance})

        if self.time is not None:
            print("TIME : ", end="")
            if avg_time_per_call < self.time:
                print_color("OKGREEN", "PASSED")
            else:
                print_color("FAIL", "FAILED")
                failure_stats.update({"time":avg_time_per_call})

        return failure_stats

    def __check_prompt(self, prompt: dict) -> None:
        required_fields = set(["name", "prompt", "calls"])

        # Check required fields
        for field in required_fields:
            if field not in prompt:
                print(prompt)
                raise (Exception(f"Missing required field '{field}' \nFor {prompt}"))

        # Check mock
        if "mock" in prompt:
            if not isinstance(prompt.get("mock"), list):
                raise (Exception("Mocks should be a list object"))

    def __set_prompt(self, prompt: dict) -> None:
        prompt_obj = prompt.get("prompt")
        if "text" in prompt_obj:
            return prompt_obj.get("text")
        elif "file" in prompt_obj:
            try:
                f = open(prompt_obj.get("file"), "r")
                data = f.read()
                f.close()
                return data
            except Exception as e:
                print(f"Something went wrong while reading file")
                raise (e)
        else:
            raise (
                Exception(f"No 'text' or 'file' field was found for prompt {self.name}")
            )

    def __set_mocks(self, prompt:dict) -> list:
        mock_data = {}
        print("Prompt", self.name)
        for mock in prompt.get("mock", []):
            if "file" not in mock:
                raise (Exception(f"Missing file field in mock for {self.name}"))
            file_name = mock.get("file")
            if not file_name.endswith(".json"):
                raise (
                    Exception(
                        f"Mock file should be JSON. Got {file_name[file_name.rfind('.'):]} in {file_name}"
                    )
                )
            mock_data[file_name] = read_json(file_name)
        return mock_data

    def _set_target(self, prompt: dict):
        target = prompt.get("target")

        if "file" not in target and "text" not in target:
            raise (Exception("Missing file or text field in target"))

        if "max" not in target:
            raise (Exception("Missing 'max' value in target"))

        if "file" in target:
            file_name = target.get("file")
            file = open(file_name, "r")
            text = file.read()
            file.close()
            return {"text": text, "max": target.get("max")}

        return {"text": target.get("text"), "max": target.get("max")}

    def _set_api_key(self, prompt: dict) -> str:
        if "key" in prompt:
            return prompt.get("key")
        elif "OPENAI_API_KEY" in os.environ:
            return os.environ.get("OPENAI_API_KEY")
        
        raise(Exception("No 'OPENAI_API_KEY' was found in environment vars"))

    def __str__(self) -> str:
        attrs = [
            x for x in dir(self) if not x.startswith("__") and not x.startswith("_")
        ]
        str_object = ""

        for attr in attrs:
            value = getattr(self, attr)
            if value is not None:
                str_object += f"{attr}: {value}\n"

        return str_object
