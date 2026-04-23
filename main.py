import argparse, os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from agent.prompts import system_prompt
from agent.call_function import available_functions
from agent.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model_name = 'gemini-2.5-flash'
conversation_history = []
max_iterations = 10

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    verbose = args.verbose
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    if api_key is None:
        raise RuntimeError('API key not set!')
    for i in range(max_iterations):
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            # config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt,
            #                                    temperature=0),
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            # contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
        )
        if response is None or response.usage_metadata is None:
            raise RuntimeError('Response not set!')
        if response.candidates:
            candidates = response.candidates
            for candidate in candidates:
                messages.append(candidate.content)

        if response is not None and response.function_calls is not None:
            function_responses = []
            for call in response.function_calls:
                print(f"Calling function: {call.name}({call.args})")
                function_call_result = call_function(call)
                if function_call_result is None or len(function_call_result.parts) == 0:
                    raise RuntimeError('Functions call stack not set!')
                if function_call_result.parts[0].function_response is None:
                    raise RuntimeError('Function call result not set!')
                if function_call_result.parts[0].function_response.response is None:
                    raise RuntimeError('Function call response is empty!')
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result)
            messages.extend(function_responses)
        else:
            print(f"Response:\n{response.text}")
            break
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(f"Max iterations ({max_iterations}) reached without a final response.")

if __name__ == "__main__":
    main()
