import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
import json
from prompt import system_prompt
from functions.call_function import available_functions,call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

parser = argparse.ArgumentParser()
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose" , action="store_true" , help="Enable verbose output")
args = parser.parse_args()

if api_key == None:
    raise Exception("no api key found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for i in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions
    )
    if response.usage == None:
        raise RuntimeError("response generation failed")

    if args.verbose:
        print("User prompt:" , args.user_prompt)
        print("Prompt tokens: " , response.usage.prompt_tokens)
        print("Response tokens: " , response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    print("response message:" , messages)


    if message.tool_calls is None:
        break

    for tool_call in message.tool_calls:
        
        result_message = call_function(tool_call , verbose=args.verbose)
        print("result messgage here: ", result_message)
        if result_message["content"] is None:
            raise Exception("")
        if args.verbose:
            print(f"-> {result_message['content']}")  

        messages.append(result_message)   

    if i == 19:
        print("something went worng")
        exit(1)

                                                                         