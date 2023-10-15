# LLM Quality Testing CLI Tool
This CLI tool operates by repeatedly prompting an LLM with the same input, capturing embeddings of the generated responses. It computes the center point within this embedding space and calculates the average Euclidean distance from the center to each response, providing a concise measure of response spread.

## Usage
```bash
main.py [-h] {spread} ...
```

## Subcommands
### Spread
Check Spread of LLM Outputs. Spread is the average Euclidean distance of embeddings prompt outputs and their centroid. 
```
python main.py spread [-h] [-f FILE] [-n CALLS] [--key KEY] [-p PROMPT] [--temperature TEMPERATURE] [--engine ENGINE]  
```

### Compare
"Compare" command takes a target output and a prompt and gives the average distance between prompt and target output. Target argument needs target text or name/path of a text file containing target text. A smaller distance indicates a higher likelihood that the prompts will generate output resembling the target.

```
python main.py compare [-h] [-f FILE] [-n CALLS] [--key KEY] [-p PROMPT] [--temperature TEMPERATURE] [--engine ENGINE] -target [text/.txt file]
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

(spread) C:\Users\pawar\Desktop\spread\src>python main.py compare -p "translate to spanish 'Hello, how are you?'" --calls 2 --temperature 0.9 --target "Test target text"
Calling OpenAI(2/2)
Distance : 0.00034403593720296695
```