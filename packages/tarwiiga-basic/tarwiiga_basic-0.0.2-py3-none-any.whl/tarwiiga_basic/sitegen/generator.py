import json
from langchain.prompts import ChatPromptTemplate
from ..llm import get_model


def get_prompt_message(user_input):
    template = """
    You are a website copy writer spicilaist, you write websites copies for small websites.
    Your copyies should be attractive, and make clients call to ask for the services.
    You will be given a short input about and website idea and your job is to generate the copy.
    For the following input, give the following example as reference:

    Example:
    ```json
    {{
        "name": "MLAcademy",
        "domain": "mlacademy",
        "url": "https://sites.tarwiiga.com/mlacademy",
        "bg_color": "#ffffff",
        "text_color": "#000000",
        "home_page": {{
            "title": "Home",
            "link": "/mlacademy",
            "headline": "Welcome to ML Academy",
            "description": "Master Machine Learning with Expert-led Courses",
            "phone_number": "01234567890"
        }},
        "page1": {{
            "title": "Our Courses",
            "link": "/mlacademy/courses",
            "headline": "Comprehensive Machine Learning Courses",
            "description": "Explore a wide range of courses to enhance your machine learning skills.",
            "phone_number": "01234567890"
        }},
        "page2": {{
            "title": "Contact Us",
            "link": "/mlacademy/contact",
            "headline": "Get in Touch",
            "description": "Contact us for more information about our machine learning courses.",
            "phone_number": "01234567890"
        }}
    }}
    ```

    only give the JSON object in the language of input

    user_input: {user_input}
    """

    prompt = ChatPromptTemplate.from_template(template=template)

    messages = prompt.format_messages(user_input=user_input)

    return messages[0]


def generate_site(user_input, selected_llm):
    model = get_model(selected_llm)
    prompt = get_prompt_message(user_input=user_input).content
    model_response = model.invoke(prompt)
    json_data = model_response.content.replace('```json', "").replace('```', "").strip()
    site = json.loads(json_data)
    return site
