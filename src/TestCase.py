from utils import read_json, print_color, get_embeddings
from controllers import spread_controller


class TestCase:
    def __init__(self, prompt) -> None:
        self.__check_prompt(prompt)

        self.name = prompt.get("name")
        self.prompt = self.__set_prompt(prompt)
        self.mocks = self.__set_mocks(prompt)
        self.calls = prompt.get("calls", None)
        self.engine = prompt.get("engine", None)
        self.temperature = prompt.get("temperature", 0.0)
        
        # Set criteria
        self.time = prompt.get("time", None)
        self.target = self._set_target(prompt) if "target" in prompt else None
        self.spread = prompt.get("spread", None)

    def test(self):
        for mock_data in self.mocks:
            print(f"Testing {self.prompt.format(**mock_data)}")

    def __check_prompt(self, prompt):
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

    def __set_prompt(self, prompt):
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

    def __set_mocks(self, prompt) -> list:
        mock_data = []
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
            mock_data.append(read_json(file_name))
        return mock_data

    def _set_target(self, prompt):
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

    