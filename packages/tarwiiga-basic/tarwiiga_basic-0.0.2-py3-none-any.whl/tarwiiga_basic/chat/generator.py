from .loader import load_db
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from ..llm import get_model


def get_chat_prompt(language_code):
    template = ""
    if language_code == "en":
        template = """
        Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer. 
        Use three sentences maximum. Keep the answer as concise as possible. 
        Always say "thanks for asking!" at the end of the answer. 
        {context}
        Question: {question}
        Helpful Answer:
        """
    elif language_code == "ar":
        template = """
        استخدم هذه الفقرات من السياق للاجابة على السؤال في النهاية.
        إذا كنت لا تعرف الاجابة، قل انك لا تعرف، لا تحاول في تخمين اجابة.
        استخدم ثلاث جمل لا اكثر، واجعل الاجابة مناسبة على قدر الامكان.
        قل دائما شكرا على السؤال في نهاية الاجابة.
        {context}
        السؤال: {question}
        الاجابة المفيدة:
        """
    return PromptTemplate.from_template(template)


def answer_query(query, llm, language_code):
    persist_directory = f"./data/chroma_db_{language_code}"
    collection_name = f"answers_{language_code}"
    db = load_db(collection_name, persist_directory, language_code)
    model = get_model(llm)
    chat_prompt = get_chat_prompt(language_code)
    chain = RetrievalQA.from_chain_type(
        model,
        retriever=db.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": chat_prompt}
    )
    result = chain({"query": query})
    return result["result"]

