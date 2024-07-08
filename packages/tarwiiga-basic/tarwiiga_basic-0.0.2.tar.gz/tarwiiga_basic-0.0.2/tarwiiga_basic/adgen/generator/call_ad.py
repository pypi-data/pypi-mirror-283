import json
from langchain.prompts import ChatPromptTemplate
from ...llm import get_model


def get_prompt_message(user_input):
    template = """
    You are a google ads spicilaist, you write ad copies for call-only ads.
    Your ads should be attractive, and make clients click to ask for the services.
    You will be given a short input about and ad idea and your job is to generate the ad.
    For the following input, give the following information:

    1. Create a `headlines` list containing 2 unique headlines with limit to 30 characters only for each headline.
    2. Create a `descriptions` list containing 2 unique descriptions with limit to 90 characters only for each description.
    3. The format should be as follows:
        "headlines": list of 2 strings.
        "descriptions": list of 2 strings.
    
    only give the JSON object in the language of input

    input: {user_input}
    """

    prompt = ChatPromptTemplate.from_template(template=template)

    messages = prompt.format_messages(user_input=user_input)

    return messages[0]


def generate_call_ad(user_input, llm):
    model = get_model(llm)
    prompt = get_prompt_message(user_input=user_input).content
    model_response = model.invoke(prompt)
    json_data = model_response.content.replace('```json', "").replace('```', "").strip()
    call_ad = json.loads(json_data)
    return call_ad
