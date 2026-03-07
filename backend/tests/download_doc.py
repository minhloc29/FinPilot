import os
from langchain_community.document_loaders import WebBaseLoader

os.environ["USER_AGENT"] = "my-rag-bot/1.0"

loader = WebBaseLoader("https://www.investopedia.com/terms/i/inflation.asp")
docs = loader.load()

print(docs[0].page_content[:500])