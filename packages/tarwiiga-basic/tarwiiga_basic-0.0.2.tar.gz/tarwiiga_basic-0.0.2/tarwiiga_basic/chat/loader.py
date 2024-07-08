from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings


def get_embedding_function(language_code):
    if language_code == "en":
        model_id = "all-mpnet-base-v2"
    elif language_code == "ar":
        model_id = "distiluse-base-multilingual-cased-v1"
    embedding_function = HuggingFaceInferenceAPIEmbeddings(
        api_key="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",
        model_name=f"sentence-transformers/{model_id}"
    )
    return embedding_function


def load_db(collection_name, persist_directory, language_code):
    embedding_function = get_embedding_function(language_code)
    db = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_function,
        persist_directory=persist_directory,
    )
    return db


