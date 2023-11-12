![Static Badge](https://img.shields.io/badge/License-MIT-blue)
![Static Badge](https://img.shields.io/badge/Version-0.0.1-green)
![Static Badge](https://img.shields.io/badge/Code_Style-black-black)
![Static Badge](https://img.shields.io/badge/Status-Work_In_Progress-brown)


# Table of Contents <!-- omit from toc --> 
- [Spread v0.0.1](#spread-v001)
  - [Getting started](#getting-started)
  - [Subcommands](#subcommands)
    - [Spread](#spread)
    - [Compare](#compare)
    - [Test](#test)
  - [Options](#options)
  - [Example](#example)
    - [**Spread**](#spread-1)
    - [**Compare**](#compare-1)
    - [**Test**](#test-1)

# Spread v0.0.1
This CLI tool operates by repeatedly prompting an LLM with the same input, capturing embeddings of the generated responses. It computes the center point within this embedding space and calculates the average Euclidean distance from the center to each response, providing a concise measure of response spread.

## Getting started
```
git clone gaurang98671/spread
cd spread
pip install -r requirements.txt
```

## Subcommands
### Spread
```spread``` command checks the Spread of LLM Outputs. Spread is the average Euclidean distance of embeddings prompt outputs and their centroid. 
```
python main.py spread [-h] [-f FILE] [-n CALLS] [--key KEY] [-p PROMPT] [--temperature TEMPERATURE] [--engine ENGINE]  
```

### Compare
```compare``` command takes a target output and a prompt and gives the average distance between prompt and target output. Target argument needs target text or name/path of a text file containing target text. A smaller distance indicates a higher likelihood that the prompts will generate output resembling the target.

```
python main.py compare [-h] [-f FILE] [-n CALLS] [--key KEY] [-p PROMPT] [--temperature TEMPERATURE] [--engine ENGINE] -target [text/.txt file]
```

### Test
```test``` command takes a .yaml file containing all test criteria. It will exit with status code **1** if any of the criteria fails.
```
python main.py test <file name>
```

## Options
| Short Flags | Long Flags| Description|
|-|-|-|
| -h  | --help         | Show this help message and exit. |
| -f  | --file         | Specify a prompt text file.      |
| -n  | --calls        | Number of calls to LLM.          |
|     | --key          | OpenAI API key.                  |
| -p  | --prompt       | Input prompt.                    |
|     | --temperature  | LLM temperature.                 |
|     | --engine       | LLM engine.                      |
|     | --log          | Add prefix to a log file         |
| -v  | --verbose      | Print verbose output             |
| -np | --nprompt      | Pass in multiple prompt files    |

## Example

### **Spread**
```
(spread) C:\Users\pawar\Desktop\spread\src>python main.py spread -p "translate to french 'Hello, how are you?'" --calls 5  
Calling OpenAI(5/5)
Spread: 0.0
```

### **Compare**
```
(spread) C:\Users\pawar\Desktop\spread\src>python main.py compare -p "translate to spanish 'Hello, how are you?'" --calls 2 --temperature 0.9 --target "Test target text"
Calling OpenAI(2/2)
Distance : 0.00034403593720296695
```

### **Test**
```
(spread) C:\Users\pawar\Desktop\spread\src>python main.py test ../examples/test.yaml
system
--------------------------------------------------
Prompt : This is a test prompt

For ../examples/mock1.json
SPREAD : FAILED
TARGET : PASSED
TIME : FAILED

For ../examples/mock2.json
SPREAD : FAILED
TARGET : PASSED
TIME : FAILED

Prompt : Summarize system in 100 words
No mock data found. Running test for prompt

TIME : PASSED

user
--------------------------------------------------
No test criteria were found

Total failures : 4
```