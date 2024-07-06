from openai import OpenAI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(f"BASE_DIR: {BASE_DIR}")
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
# print(f"dotenv_path: {dotenv_path}")

# 删除所有文件
def delete_all_files(client):
    # 获取所有文件的列表
    files = client.files.list()

    # 逐个删除文件
    for file in files.data:
        file_id = file.id
        client.files.delete(file_id)
        print(f"Deleted file: {file_id}")

# 删除所有词向量库
def delete_all_vector_stores(client):
    # 获取所有词向量库的列表
    vector_stores = client.beta.vector_stores.list()

    # 逐个删除词向量库
    for vector_store in vector_stores.data:
        vector_store_id = vector_store.id
        client.beta.vector_stores.delete(vector_store_id)
        print(f"Deleted vector store: {vector_store_id}")
        