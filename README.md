# LLM Quality Testing CLI Tool
This CLI tool operates by repeatedly prompting an LLM with the same input, capturing embeddings of the generated responses. It computes the center point within this embedding space and calculates the average Euclidean distance from the center to each response, providing a concise measure of response spread.

## Usage
```bash
main.py [-h] {spread} ...
```

## Subcommands
### Spread
Check Spread of LLM Outputs
```
main.py spread [-h] [-f FILE] [-n CALLS] [--key KEY] [-p PROMPT] [--temperature TEMPERATURE] [--engine ENGINE]
```
## Options
| Short Flags | Long Flags| Description|
|-|-|-|
| -h  | --help         | Show this help message and exit. |
| -f  | --file         | Specify a prompt text file.      |
| -n  | --calls        | Number of calls to LLM.          |
|     | --key          | Provide the OpenAI API key.      |
| -p  | --prompt       | Input prompt.                    |
|     | --temperature  | Set the LLM temperature.         |
|     | --engine       | Specify the LLM engine.          |
|     | --log          | Add prefix to a log file         |
| -v  | --verbose      | Print verbose output             |

## Example
To check the spread of LLM outputs for a given prompt, you can use the spread subcommand with appropriate options
```
(spread) C:\Users\pawar\Desktop\spread\src>python main.py spread -p "translate to french 'Hello, how are you?'" --calls 5
Calling OpenAI(5/5)
Spread: 0.0

(spread) C:\Users\pawar\Desktop\spread\src>python main.py spread -p "translate to french 'Hello, how are you?'" --calls 5 --temperature 0.90
Calling OpenAI(5/5)
Spread: 0.185
```