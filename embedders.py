from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from decouple import config


def embed_doc(article: dict):
    MARKDOWN_SEPARATORS = [
        "\n#{1,6} ",
        "```\n",
        "\n\\*\\*\\*+\n",
        "\n---+\n",
        "\n___+\n",
        "\n\n",
        "\n",
        " ",
        "",
    ]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # The maximum number of characters in a chunk: we selected this value arbitrarily
        chunk_overlap=100,  # The number of characters to overlap between chunks
        add_start_index=True,  # If `True`, includes chunk's start index in metadata
        strip_whitespace=True,  # If `True`, strips whitespace from the start and end of every document
        separators=MARKDOWN_SEPARATORS,
    )
    doc = Document(page_content=article["content"], metadata=article["metadata"])
    return text_splitter.split_documents([doc])


def insert_doc(article: dict):
    all_splits = embed_doc(article)
    client = Chroma(
        persist_directory="mojok.co.db",
        embedding_function=OpenAIEmbeddings(api_key=config("OPENAI_API_KEY")),
    )
    client.add_documents(documents=all_splits)
