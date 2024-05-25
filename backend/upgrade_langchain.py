import os

# Directory to start searching from
root_dir = 'D:/Full stack pdf analyze project/backend'

# List of tuples with old and new import paths
imports_to_update = [
    ("from langchain_community.document_loaders import PyPDFLoader", "from langchain_community.document_loaders import PyPDFLoader"),
    ("from langchain.text_splitter import RecursiveCharacterTextSplitter", "from langchain.text_splitter import RecursiveCharacterTextSplitter"),
    ("from langchain_community.embeddings import OpenAIEmbeddings", "from langchain_community.embeddings import OpenAIEmbeddings"),
    ("from langchain_community.vectorstores import FAISS", "from langchain_community.vectorstores import FAISS"),
    ("from langchain_community.chains.question_answering import load_qa_chain", "from langchain_community.chains.question_answering import load_qa_chain"),
    ("from langchain_community.llms import OpenAI", "from langchain_community.llms import OpenAI"),
    ("from langchain_community.chains import ConversationalRetrievalChain", "from langchain_community.chains import ConversationalRetrievalChain")
]

# Function to update imports in a file
def update_imports_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    for old_import, new_import in imports_to_update:
        content = content.replace(old_import, new_import)

    with open(file_path, 'w') as file:
        file.write(content)

# Walk through the directory and update imports in .py files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.py'):
            update_imports_in_file(os.path.join(subdir, file))

print("Import updates completed.")


