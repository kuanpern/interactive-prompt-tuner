## Interactive Prompt Tuner GUI

### Introduction

Prompt tuning is a technique used to improve the performance of language models, typically for specific sets of tasks.

While there are data-driven approaches such as [DSPy](https://github.com/stanfordnlp/dspy) and [TextGrad](https://github.com/zou-group/textgrad), we observe the need in many use cases the need of human-in-the-loop (HILT) prompt tuning.

This application is an attempt to build an easy-to-use user interface for non-technical users to iteractively fine-tune their prompts for specific use cases.

Note: As of current, there is no stable release of the application.


### Setup

Install dependencies:
```bash
virtualenv -ppython3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup LLM models

(pending)


### Running the Chatbot
```bash
python app.py
```