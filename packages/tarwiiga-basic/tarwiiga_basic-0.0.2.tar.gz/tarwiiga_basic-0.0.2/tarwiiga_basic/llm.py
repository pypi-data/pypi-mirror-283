from langchain_google_genai import ChatGoogleGenerativeAI


def get_model(llm):
    model = ChatGoogleGenerativeAI(
        model=llm["selected_model"],
        google_api_key=llm["api_key"]
    )
    return model


