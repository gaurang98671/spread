# LLM Quality Testing CLI Tool

A simple command-line tool to test the quality of LLM prompts.

## Usage

```bash
main.py [-h] {spread} ...
```

## Subcommands
Check Spread of LLM Outputs
```
main.py spread [-h] [-f FILE] [-n CALLS] [--key KEY] [-p PROMPT] [--temperature TEMPERATURE] [--engine ENGINE]
```
### Options
* -h, --help: Show this help message and exit.
* -f FILE, --file FILE: Specify a prompt text file.
* -n CALLS, --calls CALLS: Number of calls to LLM.
* --key KEY: Provide the OpenAI API key.
* -p PROMPT, --prompt PROMPT: Input prompt.
* --temperature TEMPERATURE: Set the LLM temperature.
* --engine ENGINE: Specify the LLM engine.

## Example
To check the spread of LLM outputs for a given prompt, you can use the spread subcommand with appropriate options
```
(spread) C:\Users\pawar\Desktop\spread\src>python main.py spread -p "translate to french 'Hello, how are you?'" --calls 5
Calling OpenAI(5/5)
Score: 0.0

(spread) C:\Users\pawar\Desktop\spread\src>python main.py spread -p "translate to french 'Hello, how are you?'" --calls 5 --temperature 0.90
Calling OpenAI(5/5)
Score: 0.185
```