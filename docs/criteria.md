
# Table of Contents <!-- omit from toc --> 
- [Criteria](#criteria)
  - [Spread](#spread)
      - [Visualization](#visualization)
    - [Example](#example)
  - [Target](#target)
    - [Example](#example-1)
  - [Time](#time)
    - [Example](#example-2)
  - [Regex](#regex)
    - [Example](#example-3)
  - [Tokens](#tokens)
    - [Example](#example-4)

# Criteria
You can test for multiple criteria, each having a specific keyword and a corresponding value for comparison. Prompt responses will be compared with these values to assess the test criteria.

## Spread
The `spread` criterion will assess the spread value of all responses. The spread value represents the unit of how much prompt responses are diverged from each other. A **spread of 0** implies that the prompt will consistently yield the same value.

#### Visualization
![Spread](../examples/spread_visulization.gif)

### Example
```
system:
  - name: Test prompt to check spread criteria
    prompts:
      - name: Test Prompt
        prompt:
          text: This is a test prompt reply with random text response
        calls: 10
        spread: 0
```

## Target
```target``` requires 2 sub-pdarameters **text/file** and **min**. It will compare text with the prompt output to get [Jaro similarity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) score. Test case will fail if this score is less than **min** value

### Example
```
regex_check:
  - name: Example prompt to test target criteria
    prompts:
      - name: Check target
        calls: 1
        temperature: 0
        prompt:
          file: ../examples/regex/regex_prompt.txt
        target:
            text: "<>\asdnaskjdnaijsdnijasnijdnn"
            min: 1.0
```

## Time
```time``` will check average time in seconds for each response for n calls. Following is an example manifest.

### Example
```
check_time:
  - name: Test prompt to check time
    prompts:
      - name: Test prompt to check time
        calls: 10
        temperature: 0.6
        prompt:
          text: Write me a 500-word college essay.
        time: 5
```

## Regex
```regex``` criteria checks prompt outputs with a regular expression. Here is an example manifest for checking regex.

### Example
```regex_check:
  - name: Regex check prompt
    prompts:
      - name: Check regex
        calls: 2
        temperature: 0
        prompt:
          text: Return '<>' character as response. Only return mentioned characters and nothing else.
        regex: "<>"

```

## Tokens

### Example
```

```
