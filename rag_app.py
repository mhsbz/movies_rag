import chromadb
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI


os.environ["TOKENIZERS_PARALLELISM"] = "false"
### init vector database
print("load vector processing...")
chroma_client = chromadb.HttpClient(
        host='localhost',
        port=8000
    )

### init embedding model
print("load embedding model processing...")
embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

### init data loader
print("init data loader processing...")
# 使用DirectoryLoader加载文档
loader = DirectoryLoader("knowledge_base", glob="**/*.txt")
docs = loader.load()

# 不进行分块处理，保持整篇文档完整
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100000, chunk_overlap=0)
split_docs = text_splitter.split_documents(docs)

# 创建向量存储
vectorstore = Chroma(
    collection_name="movies",
    embedding_function=embed_model,
    client=chroma_client,
    persist_directory="./chroma_data"
)

# 如果向量存储为空，则添加文档
if vectorstore._collection.count() == 0:
    print("Adding documents to vectorstore...")
    vectorstore.add_documents(split_docs)

def query_qusetion(q: str) ->str:
    reference_docs = vectorstore.search(query=q,search_type="similarity",k=3)

    context = ""

    idx = 0
    for item in reference_docs:
        page_content = item.page_content.replace("\n\n","\n")
        context += f"参考文档{idx}:\n{page_content}\n\n"
        idx += 1

    # 创建自定义提示模板
    prompt = """你是一个专业的电影知识助手。请基于以下参考文档回答用户的问题。
    如果参考文档中没有相关信息，请直接回复"抱歉，我没有找到相关信息"。
    请记住：只回答与参考文档相关的内容，不要编造信息。

    参考文档:
    {context}

    我的问题是:
    {question}
    """

    client = OpenAI(api_key="sk-1be1fd22019d428aac229e420d2be812", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt.format(context=context,question=q)},
        ],
        stream=False
    )

    # print("context: ",context)

    return response.choices[0].message.content

if __name__ == '__main__':
    while True:
        q = input("请输入要查询的电影：")
        if q == "/bye":
            break
        print(query_qusetion(q))

