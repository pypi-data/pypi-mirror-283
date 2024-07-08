import json
from langchain.prompts import ChatPromptTemplate
from ...llm import get_model


def get_ad_prompt_message(user_input):
    template = """
    You are a Google Ads specialist that craft an Ad copy for {user_input} that reach new customers.
    Generate a JSON object for a Google responsive search ad with the following requirements:
    
    1. Create a `headlines` list containing 15 unique headlines with limit to 30 characters only for each headline.
    2. Create a `descriptions` list containing 4 unique descriptions with limit to 90 characters only for each description.
    3. The format should be as follows:
        "headlines": list of 15 strings.
        "descriptions": list of 4 strings.
    
    only give the JSON object in the language of input and like this format:
    ```json
    {{
        "headlines": list of 15 unique strings.
        "descriptions": list of 4 unique strings.
    }}
    ```

    user_input: {user_input}
    """

    prompt = ChatPromptTemplate.from_template(template=template)

    messages = prompt.format_messages(user_input=user_input)

    return messages[0]


def get_ads_combination_prompt_message(user_input):
    template = """
    Generate a JSON object containing a list of Google responsive search ads. 

    Each ad should include:
    2 unique headlines from a given set of 15 headlines.
    2 unique descriptions from a given set of 4 descriptions.
    The format should be as follows:
        "headlines": list of 2 strings.
        "descriptions": list of 2 strings.
            
    Use the following sets for headlines and descriptions: {user_input}
    
    Make combinations of headlines and descriptions and give list of 8 ads
    
    only give the JSON object in the language of input in this format:
    ```json
    [
        {{
            "headlines": list of 2 strings.
            "descriptions": list of 2 strings.
        }}
    ]
    ```
    """

    prompt = ChatPromptTemplate.from_template(template=template)

    messages = prompt.format_messages(user_input=user_input)

    return messages[0]


def generate_responsive_ads(user_input, selected_llm):
    model = get_model(selected_llm)
    prompt = get_ad_prompt_message(user_input=user_input).content
    model_response = model.invoke(prompt)
    json_data = model_response.content.replace('```json', "").replace('```', "").strip()
    responsive_ad = json.loads(json_data)

    prompt = get_ads_combination_prompt_message(user_input=responsive_ad).content
    model_response = model.invoke(prompt)
    json_data = model_response.content.replace('```json', "").replace('```', "").strip()
    responsive_ads = json.loads(json_data)

    return responsive_ad, responsive_ads
