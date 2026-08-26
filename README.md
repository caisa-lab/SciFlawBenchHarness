# SciFlawBench Harness

## descriptions
This repository is mean to be a harness from which to run the sciflaw benchmark for models within an agentic context at the university of Bonn. It is built on top of smolagents and has a multiprocess architechture to allow for **blazingly** fast running of the benchmark

## code repository overview

```
src/
├── core/
│   ├── config.py               # base types used for parsing the config (w/ pydantic)
│   ├── events.py               # defines event watchers and base event primitives
│   ├── manager.py              # runtime manager code that handles dispatching subprocesses
│   ├── registry.py             # registry code which is reused for agent and tool registry (handles mapping string -> obj factory)
│   └── tasks.py                # definition for task primiteves and contains teh run_task function used for actual task runs
├── agents/
│   ├── prompts/
│   │   └── default.yaml        # defailt prompt associated wiht default agent
│   ├── prompts.py              # right now just containes a load prompt file
│   ├── definitions.py          # definitions of base agents to be used in testing and agent registry
│   └── base.py                 # contains build_agent function
├── evaluation/
│   ├── print_report.py         # contains logic pertaining to converting reports into markdown 
│   ├── definitions.py          # definitions of verifiers and the verifier registry
│   └── base.py                 # defines basic necessary structures for validation code
├── models/
│   └── base.py                 # defines how to build a model and model wrapper
├── tools/
│   ├── custom.py               # custom tool classes that get registered
│   ├── definitions.py          # all custom tool definitions and wrapper/registry definiotion for use in pipeline
│   └── base.py                 # containes wrapper for use on all tools 
└── main.py                     # main entrypoint for running testing harness
```

## How to use

1. clone the repository and cd in
```bash 
git clone git@github.com:ivzx04/SciFlawBenchHarness.git && cd SciFlawBenchHarness
```
2. Create a virtual environment for this project and enter the environment(optional)
```bash
python -m venv <name-of-your-venv>  && source <name-of-your-venv>/bin/activate
```
3. pip install the enviornment and dependencies
```bash 
pip install .
```
4. Write the config file in config.json with your specific model access credentials/settings
5. export the api key environment variables associated with your model providers
6. run src/main.py with your config path
```bash
python src/main.py --config /path/to/your/config
```

## Check out our Google Colab from which you can run this as well

https://colab.research.google.com/drive/1ctDfb7he22O-ipqqhIxSmfM40fEOTWXI?usp=sharing

## FAQ

1. how do I define a test task to try and run? 

    For an arbitrary task one only needs to define 3 fields for the harness to run: 
        "task_id": int 
        "task": str 
        "agent_id": Literal_string["code_agent", "tool_agent"]

2. What provider should i use for a given model / how should i configure my settings for this ?

    This largely depends on what kind of API you are hitting where the model is hosted. The most standard provider type
    is the openai_server, which is compatible with many sorts of providers including openai itself, vllm, etc.

    Currently this code base supports two other types of providers as well, those being litellm and huggingfaces own api.

    Almost all configuration options for these specific providers are documented at the following link: 
    https://deepwiki.com/huggingface/smolagents/4.2-api-based-models

    and can be specified via the extra_kwargs section in the model config. 

