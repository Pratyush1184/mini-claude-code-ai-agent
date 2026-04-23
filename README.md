# mini-claude-code
A limited functionality clone of Claude Code using Google Gemini's free tier model. It relies on a limited set of tools(functions) that we add to the repository.

# Running the code:
Go to the repository root and run the following commands:

Create a .env file with the following content:
```bash
GEMINI_API_KEY='your_api_key_here'
```
You can obtain your API key from the Google AI Studio(https://aistudio.google.com/api-keys) or create a new one.
Make sure to replace 'your_api_key_here'

Create a virtual environment:
```bash
uv venv
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Now run the application with your prompt:
```bash
uv run main.py "Your prompt here"
```

An example prompt could be:
```bash
uv run main.py "Give me the value of 3 + 7 * 2 using the calculator app I designed. Also fix the bug if the expression
evaluation is incorrect"
```

You can try introducing a bug in the calculator and then prompt the agent to evaluate, verify and then fix the bug in
the calculator code. The agent will use the tools we have provided to it to achieve the task. You can also add more
tools to the repository and the agent will be able to use them as well.
