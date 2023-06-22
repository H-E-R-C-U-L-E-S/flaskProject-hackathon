import json
import openai
from database import Database
from semantic_search import semantic_search
from translate import to_ka

api_key = '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'
openai.api_key = api_key

messages: list[dict] = [{"role": "system",
                         "content": "As an efficient human assistant, you help users find products for themselves or as gifts by utilizing semantic search in the database."}, ]


def search(query: str, type, brand='', min_price=0, max_price=''):
    db = Database()

    if brand:
        return semantic_search(query, db.filter_by_brand(brand))
    elif min_price or max_price:
        return semantic_search(query, db.filter_by_price(max_price, min_price))
    else:
        return semantic_search(query, db.filter_by_type(type))


functions = [
    {
        "name": "search",
        "description": "Finds the item according to query and user preferences",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Item description user is looking for.",
                },
                "type": {"type": "string", "description": "product type user wants","enum":["mobile_phone","laptop","washing_machine"] },
                "brand": {"type": "string", "description": "phone brand user wants.", },
                "min_price": {"type": "string", "description": "min price of phone", },
                "max_price": {"type": "string", "description": "max price of phone", },
            },
            "required": ["query", "type"],
        },
    }
]


def run_conversation(prompt):
    messages.append({'role': 'user', 'content': prompt})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature=0.7
    )

    response_message = response["choices"][0]["message"]
    print(response_message)

    if response_message.get("function_call"):
        print('func called')
        available_functions = {"search": search, }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            query=function_args.get("query"),
            type=function_args.get("type"),
            brand=function_args.get("brand"),
            min_price=function_args.get("min_price"),
            max_price=function_args.get("max_price"), )

        messages.append(response_message)
        print(response_message)
        messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response,
        })

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        response_message = second_response["choices"][0]["message"]['content']
        print(response_message)
        # print( en_to_ka(str(response_message)))
        return to_ka(str(response_message))
    return str(to_ka(response_message['content']))


def get_answer(prompt: str):
    return run_conversation(prompt)
