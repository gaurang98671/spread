from utils import read_json

class TestCase():
    def __init__(self, prompt) -> None:
        self.__check_prompt(prompt)

        self.name = prompt.get("name")
        self.prompt = self.__set_prompt(prompt)
        self.mocks = self.__set_mocks(prompt)
        self.criteria = self.__set_criteria(prompt)

    def __check_prompt(self, prompt):
        required_fields = set("name", "prompt", "criteria")

        # Check required fields
        for field in required_fields:
            if field not in prompt:
                raise(Exception(f"Missing required field {field}"))
        
        # Handle unknown fields
        for field in prompt:
            if field not in required_fields:
                raise(Exception(f"Unknown field {field}"))
        
        # Check mock
        if "mock" in prompt:
            if not isinstance(prompt.get("mock"), list):
                raise(Exception("Mocks should be a list object"))
        

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
                raise(e)
        else:
            raise(Exception(f"No 'text' or 'file' field was found for prompt {self.name}"))

    def __set_mocks(self, prompt):
        
        mock_data = []
        for mock in prompt.get("mock", []):
            if "file" not in mock:
                raise(Exception(f"Missing file field in mock for {self.name}"))
            file_name = mock.get("file")
            mock_data.append(read_json(file_name))
        return mock_data
            

    def _set_criteria(self, prompt):
        pass

