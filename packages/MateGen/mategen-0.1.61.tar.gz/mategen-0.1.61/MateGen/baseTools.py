from IPython.display import display, Code, Markdown, Image
from IPython import get_ipython
import time
import openai
import os
import json
from openai import OpenAI
from openai import OpenAIError
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime
from pathlib import Path
import oss2
from dotenv import load_dotenv, set_key, find_dotenv
import pymysql
import io
import uuid
import re
import glob
import shutil
import inspect
import requests
import random
import string
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser
import tiktoken
from lxml import etree
import sys
from cryptography.fernet import Fernet
import numpy as np
import pandas as pd
import html2text
import subprocess
import zipfile
import nbconvert
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(f"BASE_DIR: {BASE_DIR}")
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)
# print(f"dotenv_path: {dotenv_path}")

from .getProfile import *
from .mainFunc import *

def get_id(keyword):
    load_dotenv()
    headers_json = os.getenv('HEADERS')
    cookies_json = os.getenv('COOKIES')
        
    headers = json.loads(headers_json)
    cookies = json.loads(cookies_json)
    
    url = "https://www.kaggle.com/api/i/search.SearchWebService/FullSearchWeb"
    data = {
        "query": keyword,
        "page": 1,
        "resultsPerPage": 20,
        "showPrivate": True
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data).json()

    # 确保搜索结果不为空
    if "documents" not in response or len(response["documents"]) == 0:
        print(f"竞赛： '{keyword}' 并不存在，请登录Kaggle官网并检查赛题是否正确：https://www.kaggle.com/")
        return None

    document = response["documents"][0]
    document_type = document["documentType"]

    if document_type == "COMPETITION":
        item_id = document["databaseId"]
    elif document_type == "KERNEL":
        item_id = document['kernelInfo']['dataSources'][0]['reference']['sourceId']
    else:
        print(f"竞赛： '{keyword}' 并不存在，请登录Kaggle官网并检查赛题是否正确：https://www.kaggle.com/")
        return None

    return item_id

def create_kaggle_project_directory(competition_name):
    # 创建kaggle知识库目录
    kaggle_dir = create_knowledge_base_folder(sub_folder_name=competition_name)
    
    # 如果 .kaggle 目录不存在，则创建
    # if not os.path.exists(kaggle_dir):
        # os.makedirs(kaggle_dir)
        # print(f"Created directory: {kaggle_dir}")
    
    # 定义项目目录结构
    # base_dir = os.path.join(kaggle_dir, f"{competition_name}_project")
    # directories = [
        # os.path.join(base_dir, 'knowledge_library'),
        # os.path.join(base_dir, 'data'),
        # os.path.join(base_dir, 'submission'),
        # os.path.join(base_dir, 'module')
    # ]
    # task_schedule_file = os.path.join(base_dir, 'task_schedule.json')

    # 创建目录和文件
    # for directory in directories:
        # if not os.path.exists(directory):
            # os.makedirs(directory)

    # if not os.path.exists(task_schedule_file):
        # with open(task_schedule_file, 'w') as f:
            # json.dump({}, f)  
            
    # print("已完成项目创建")
    return kaggle_dir
    
def getOverviewAndDescription(_id):
    load_dotenv()
    headers_json = os.getenv('HEADERS')
    cookies_json = os.getenv('COOKIES')
        
    headers = json.loads(headers_json)
    cookies = json.loads(cookies_json)
    url = "https://www.kaggle.com/api/i/competitions.PageService/ListPages"
    data = {
        "competitionId": _id
    }
    data = json.dumps(data, separators=(',', ':'))
    data = requests.post(url, headers=headers, cookies=cookies, data=data).json()
    overview={}
    data_description={}
    for page in data['pages']:
        # print(page['name'])
        overview[page['name']]=page['content']   
    if 'rules' in overview: del overview['rules']
    if 'data-description' in overview: 
        data_description['data-description']=overview['data-description']
        del overview['data-description']
 
    return overview, data_description

def json_to_markdown(json_obj, level=1):
    markdown_str = ""
    
    for key, value in json_obj.items():
        if isinstance(value, dict):
            markdown_str += f"{'#' * level} {key}\n\n"
            markdown_str += json_to_markdown(value, level + 1)
        else:
            markdown_str += f"{'#' * level} {key}\n\n{value}\n\n"
    
    return markdown_str

def convert_html_to_markdown(html_content):
    """
    将 HTML 内容转换为 Markdown 格式

    :param html_content: 包含 HTML 标签的文本内容
    :return: 转换后的 Markdown 文本
    """
    h = html2text.HTML2Text()
    h.ignore_links = False  # 设置为 False 以保留链接
    markdown_content = h.handle(html_content)
    return markdown_content

def save_markdown(content, competition_name, file_type):
    # home_dir = str(Path.home())
    # directory = os.path.join(os.path.expanduser(home_dir), f'.kaggle./{competition_name}_project/knowledge_library')
    directory = create_kaggle_project_directory(competition_name)
    filename = f'{competition_name}_{file_type}.md'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
def get_code(_id):
    load_dotenv()
    headers_json = os.getenv('HEADERS')
    cookies_json = os.getenv('COOKIES')
        
    headers = json.loads(headers_json)
    cookies = json.loads(cookies_json)
    data = {
        "kernelFilterCriteria": {
            "search": "",
            "listRequest": {
                "competitionId": _id,
                "sortBy": "VOTE_COUNT",
                "pageSize": 20,
                "group": "EVERYONE",
                "page": 1,
                "modelIds": [],
                "modelInstanceIds": [],
                "excludeKernelIds": [],
                "tagIds": "",
                "excludeResultsFilesOutputs": False,
                "wantOutputFiles": False,
                "excludeNonAccessedDatasources": True
            }
        },
        "detailFilterCriteria": {
            "deletedAccessBehavior": "RETURN_NOTHING",
            "unauthorizedAccessBehavior": "RETURN_NOTHING",
            "excludeResultsFilesOutputs": False,
            "wantOutputFiles": False,
            "kernelIds": [],
            "outputFileTypes": [],
            "includeInvalidDataSources": False
        },
        "readMask": "pinnedKernels"
    }
    url="https://www.kaggle.com/api/i/kernels.KernelsService/ListKernels"
    data = json.dumps(data, separators=(',', ':'))
    kernels = requests.post(url, headers=headers, cookies=cookies, data=data).json()['kernels']

    res=[]
    for kernel in kernels:
        temp={}
        temp['title']=kernel['title']
        temp['scriptUrl']="https://www.kaggle.com"+kernel['scriptUrl']
        res.append(temp)
    res = res[:10]
    return json.dumps(res)

def extract_and_transform_urls(json_urls):

    # 解析 JSON 字符串
    data = json.loads(json_urls)
    
    # 提取并转换 URL
    urls = []
    for item in data:
        url = item.get("scriptUrl", "")
        match = re.search(r"https://www.kaggle.com/code/(.*)", url)
        if match:
            urls.append(match.group(1))
    
    return urls

def download_and_convert_kernels(urls, competition_name):
    # home_dir = str(Path.home())
    # output_dir = os.path.join(os.path.expanduser(home_dir), f'.kaggle/{competition_name}_project/knowledge_library')
    output_dir = create_kaggle_project_directory(competition_name)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for kernel_path in urls:
        try:
            # 下载 Kernel
            res = subprocess.run(["kaggle", "kernels", "pull", kernel_path, "-p", output_dir], check=True)
            
            # 找到下载的 .ipynb 文件
            ipynb_file = os.path.join(output_dir, f"{os.path.basename(kernel_path)}.ipynb")
            
            if os.path.exists(ipynb_file):
                # 转换 .ipynb 文件为 .md 文件
                try:
                    md_exporter = nbconvert.MarkdownExporter()
                    md_data, resources = md_exporter.from_filename(ipynb_file)
                    
                    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(ipynb_file))[0] + '.md')
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(md_data)
                    #print(f"Converted {ipynb_file} to {output_file}")
                    
                    # 删除原 .ipynb 文件
                    os.remove(ipynb_file)
                    #print(f"Deleted {ipynb_file}")
                except Exception as e:
                    print(f"Error converting {ipynb_file}: {e}")
                    traceback.print_exc()
            else:
                # print(f"{ipynb_file} not found, skipping conversion.")
                pass
            time.sleep(1)  # 避免请求过于频繁

        except subprocess.CalledProcessError as e:
            # print(f"Error downloading kernel {kernel_path}: {e}")
            traceback.print_exc()

    return 'done'

def check_knowledge_base_name(client, knowledge_base_name):
    vector_stores = client.beta.vector_stores.list()
    for vs in vector_stores.data:
        if vs.name == knowledge_base_name:
            return vs.id
    return None


def create_knowledge_base_folder(sub_folder_name=None):
    # 找到 .env 文件路径
    dotenv_path = find_dotenv()
    
    # 加载 .env 文件
    if dotenv_path:
        load_dotenv(dotenv_path)

    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')
    
    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')

    # 创建 base_path 文件夹
    os.makedirs(base_path, exist_ok=True)

    # 检查并创建主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        with open(main_json_file, 'w') as f:
            json.dump({}, f, indent=4)

    # 如果 sub_folder_name 不为空，则在 base_path 内创建子文件夹
    if sub_folder_name:
        sub_folder_path = os.path.join(base_path, sub_folder_name)
        os.makedirs(sub_folder_path, exist_ok=True)

        # 检查并创建子目录 JSON 文件
        sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')
        if not os.path.exists(sub_json_file):
            with open(sub_json_file, 'w') as f:
                json.dump({"vector_db_id": -1}, f, indent=4)

        return sub_folder_path
    else:
        return base_path

def update_vector_db_mapping(sub_folder_name, vector_db_id):
    # 确保主目录和子目录及其JSON文件存在
    sub_folder_path = create_knowledge_base_folder(sub_folder_name)
    
    # 获取主目录路径和JSON文件路径
    base_path = os.path.dirname(sub_folder_path)
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    
    # 更新主目录JSON文件
    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)
    
    main_mapping[sub_folder_name] = vector_db_id
    
    with open(main_json_file, 'w') as f:
        json.dump(main_mapping, f, indent=4)
    
    # 更新子目录JSON文件
    sub_json_file = os.path.join(sub_folder_path, f'{sub_folder_name}_vector_id.json')
    
    with open(sub_json_file, 'r') as f:
        sub_mapping = json.load(f)
    
    sub_mapping["vector_db_id"] = vector_db_id
    
    with open(sub_json_file, 'w') as f:
        json.dump(sub_mapping, f, indent=4)  

def print_and_select_knowledge_base():
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')
    
    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')
    
    # 检查主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        print(f"{main_json_file} 不存在。请先创建知识库。")
        return None, None
    
    # 读取主目录 JSON 文件
    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)
    
    # 打印所有知识库名称
    print("知识库列表：")
    knowledge_bases = list(main_mapping.keys())
    for idx, name in enumerate(knowledge_bases, 1):
        print(f"{idx}. {name}")
    
    # 用户选择知识库
    selection = int(input("请选择一个知识库的序号：")) - 1
    if selection < 0 or selection >= len(knowledge_bases):
        print("无效的选择。")
        return None, None
    
    selected_knowledge_base = knowledge_bases[selection]
    vector_db_id = main_mapping[selected_knowledge_base]   
    
    return selected_knowledge_base, vector_db_id
    
def get_specific_files(folder_path):
    # 指定需要过滤的文件扩展名
    file_extensions = ['.md', '.pdf', '.doc', '.docx', '.ppt', '.pptx']
    
    file_paths = [
        os.path.join(folder_path, file) 
        for file in os.listdir(folder_path) 
        if os.path.isfile(os.path.join(folder_path, file)) and any(file.endswith(ext) for ext in file_extensions)
    ]
    return file_paths

def create_knowledge_base(client, knowledge_base_name, folder_path_base = None):
    
    print("正在创建知识库，请稍后...")
    sub_folder_name = knowledge_base_name
    if folder_path_base == None:
        folder_path = create_knowledge_base_folder(sub_folder_name=knowledge_base_name)
    else:
        folder_path = folder_path_base
    knowledge_base_name = knowledge_base_name + '!!' + client.api_key[8: ]
    vector_stores = client.beta.vector_stores.list()
    
    vector_id = None
    # expires_after = {
        # "anchor": "last_active_at",  
        # "days": 1  
    # }
    
    for vs in vector_stores.data:
        if vs.name == knowledge_base_name:
            vector_store_files = client.beta.vector_stores.files.list(
                vector_store_id=vs.id
            )
            for file in vector_store_files.data:
                file = client.beta.vector_stores.files.delete(
                    vector_store_id=vs.id,
                    file_id=file.id
                )
                client.files.delete(file.id)
            vector_id = vs.id
       
    print("正在创建知识库的向量存储，请稍后...")
    if vector_id == None:
        vector_store = client.beta.vector_stores.create(name=knowledge_base_name)
        
        vector_id = vector_store.id
        
    try:
        file_paths = get_specific_files(folder_path)
        file_streams = [open(path, "rb") for path in file_paths]
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_id, files=file_streams
        )
    except Exception as e:
        print("知识库无法创建，请再次确认知识库文件夹中存在格式合规的文件")
        return None
    
    # dotenv_path = find_dotenv()
    # if not dotenv_path:
        # with open('.env', 'w', encoding='utf-8') as f:
            # pass
        # dotenv_path = find_dotenv()


    # load_dotenv(dotenv_path)
    # specific_base_var = knowledge_base_name + "_vector_id"
    # os.environ[specific_base_var] = vector_id

    # set_key(dotenv_path, specific_base_var, os.environ[specific_base_var])
    if folder_path_base != None:
        update_vector_db_mapping(sub_folder_name=sub_folder_name, 
                                 vector_db_id=vector_id)
    print("知识库创建完成！")
    return vector_id

def clear_folder(folder_path):
    """
    删除指定文件夹内的全部内容
    :param folder_path: 要清空的文件夹路径
    """
    # 检查文件夹是否存在
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # 删除文件夹内的全部内容
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或符号链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 删除目录
            except Exception as e:
                pass
                # print(f"Failed to delete {file_path}. Reason: {e}")
        # print(f"清空了文件夹: {folder_path}")
    else:
        # print(f"文件夹不存在或不是一个目录: {folder_path}")
        pass

def create_competition_knowledge_base(competition_name, client):
    try:
        load_dotenv()
        headers_json = os.getenv('HEADERS')
        cookies_json = os.getenv('COOKIES')
        
        headers = json.loads(headers_json)
        cookies = json.loads(cookies_json)
        
        _id = get_id(keyword=competition_name)
        
        if _id:
            folder_path = create_kaggle_project_directory(competition_name)
            print(f"已找到指定竞赛{competition_name}，正在检索支持库是否存在竞赛信息...")
            knowledge_base_name = competition_name + '!!' + client.api_key[8:]
            knowledge_base_check = check_knowledge_base_name(client=client, knowledge_base_name=knowledge_base_name)
            if knowledge_base_check:
                user_input = input('检测到存在该赛题知识库，是否更新知识库（1），或者直接使用该知识库（2）：')
                if user_input == '2':
                    return knowledge_base_check
                else:
                    print("即将更新知识库...")
                    # create_knowledge_base(client=client, knowledge_base_name=competition_name)
                    # client.beta.vector_stores.delete(vector_store_id=knowledge_base_check)
                    clear_folder(create_kaggle_project_directory(competition_name))
            
            print("正在准备构建知识库...")
            create_kaggle_project_directory(competition_name = competition_name)
            overview, data_description = getOverviewAndDescription(_id)
            print("正在获取竞赛说明及数据集说明...")
            overview_md = convert_html_to_markdown(json_to_markdown(overview))
            data_description_md = convert_html_to_markdown(json_to_markdown(data_description))
            save_markdown(content=overview_md, competition_name=competition_name, file_type='overview')
            save_markdown(content=data_description_md, competition_name=competition_name, file_type='data_description')
            print(f"正在获取{competition_name}竞赛热门kernel...")
            json_urls = get_code(_id)
            urls = extract_and_transform_urls(json_urls=json_urls)
            res = download_and_convert_kernels(urls=urls, competition_name=competition_name)
            print("知识文档创建完成，正在进行词向量化处理与存储，请稍后...")
            # home_dir = str(Path.home())
            # folder_path = os.path.join(os.path.expanduser(home_dir), f'.kaggle./{competition_name}_project/knowledge_library')
            
            # vector_store = client.beta.vector_stores.create(name=knowledge_base_name)
            # file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
            # md_files = [file for file in file_paths if file.endswith('.md')]
            # file_streams = [open(path, "rb") for path in md_files]
            # file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                # vector_store_id=vector_store.id, files=file_streams
            # )
            vector_store_id = create_knowledge_base(client=client, knowledge_base_name=competition_name)
            print("已顺利完成Kaggle竞赛知识库创建，后续可调用知识库回答。")
            return vector_store_id
        else:
            print("找不到对应的竞赛，请检查竞赛名称再试。")
            return None
    except Exception as e:
        print("服务器拥挤，请稍后再试...")
        return None
    


def python_inter(py_code, g='globals()'):
    """
    专门用于执行python代码，并获取最终查询或处理结果。
    :param py_code: 字符串形式的Python代码，
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：代码运行的最终结果
    """    
    try:
        # 尝试如果是表达式，则返回表达式运行结果
        return str(eval(py_code, g))
    # 若报错，则先测试是否是对相同变量重复赋值
    except Exception as e:
        global_vars_before = set(g.keys())
        try:            
            exec(py_code, g)
        except Exception as e:
            return f"代码执行时报错{e}"
        global_vars_after = set(g.keys())
        new_vars = global_vars_after - global_vars_before
        # 若存在新变量
        if new_vars:
            result = {var: g[var] for var in new_vars}
            return str(result)
        else:
            return "已经顺利执行代码"
             

def sql_inter(sql_query, g='globals()'):
    """
    用于执行一段SQL代码，并最终获取SQL代码执行结果，\
    核心功能是将输入的SQL代码传输至MySQL环境中进行运行，\
    并最终返回SQL代码运行结果。需要注意的是，本函数是借助pymysql来连接MySQL数据库。
    :param sql_query: 字符串形式的SQL查询语句，用于执行对MySQL中telco_db数据库中各张表进行查询，并获得各表中的各类相关信息
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：sql_query在MySQL中的运行结果。
    """
    
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    host = os.getenv('HOST')
    user = os.getenv('USER')
    mysql_pw = os.getenv('MYSQL_PW')
    db = os.getenv('DB')
    port = os.getenv('PORT')
    
    connection = pymysql.connect(
        host = host,  
        user = user, 
        passwd = mysql_pw,  
        db = db,
        port = int(port),
        charset='utf8',
    )
    
    try:
        with connection.cursor() as cursor:
            sql = sql_query
            cursor.execute(sql)
            results = cursor.fetchall()

    finally:
        connection.close()

    return json.dumps(results)

def extract_data(sql_query, df_name, g='globals()'):
    """
    借助pymysql将MySQL中的某张表读取并保存到本地Python环境中。
    :param sql_query: 字符串形式的SQL查询语句，用于提取MySQL中的某张表。
    :param df_name: 将MySQL数据库中提取的表格进行本地保存时的变量名，以字符串形式表示。
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：表格读取和保存结果
    """
    
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    host = os.getenv('HOST')
    user = os.getenv('USER')
    mysql_pw = os.getenv('MYSQL_PW')
    db = os.getenv('DB')
    port = os.getenv('PORT')
    
    connection = pymysql.connect(
        host = host,  
        user = user, 
        passwd = mysql_pw,  
        db = db,
        port = int(port),
        charset='utf8',
    )
    
    g[df_name] = pd.read_sql(sql_query, connection)
    
    return "已成功完成%s变量创建" % df_name

def generate_object_name(base_name="fig", use_uuid=True):
    """
    生成对象名称，可以选择使用UUID或日期时间。

    :param base_name: 基础名称
    :param use_uuid: 是否使用UUID
    :return: 生成的对象名称
    """
    if use_uuid:
        object_name = f"{base_name}_{uuid.uuid4().hex}.png"
    else:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"{base_name}_{current_time}.png"
    return object_name

def upload_fig_to_oss(fig, object_name=None):
    """
    上传fig对象到阿里云OSS并返回图片的URL

    :param fig: Matplotlib的fig对象
    :param object_name: OSS中的文件路径和名称
    :return: 上传后图片的URL
    """
    if object_name is None:
        object_name = generate_object_name()

    try:
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        
        access_key_id = os.getenv('ACCESS_KEY_ID')
        access_key_secret = os.getenv('ACCESS_KEY_SECRET')
        endpoint = os.getenv('ENDPOINT')
        bucket_name = os.getenv('BUCKET_NAME')
        
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        
        # 将fig对象保存到内存中的字节流
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)  # 将字节流指针重置到起始位置
        
        # 上传字节流到OSS
        bucket.put_object(object_name, buffer)

        # 构建图片URL
        match = re.search(r'(oss[^/]*)', bucket.endpoint)
        endpoint_url = match.group(1)
        url = f"https://{bucket.bucket_name}.{endpoint_url}/{object_name}"
        print(f"Figure uploaded to OSS as {object_name}")
        return url
    except Exception as e:
        print(f"Failed to upload figure: {e}")
        return None

def fig_inter(py_code, fname, g='globals()'):
    """
    用于执行一段包含可视化绘图的Python代码，并最终获取一个图片类型对象，并上传至阿里云oss
    :param py_code: 字符串形式的Python代码，用于根据需求进行绘图，代码中必须包含Figure对象创建过程
    :param fname: py_code代码中创建的Figure变量名，以字符串形式表示。
    :param g: g，字符串形式变量，表示环境变量，无需设置，保持默认参数即可
    :return：代码运行的最终结果，若顺利创建图片并上传至oss，则返回图片的url地址
    """    
    # 保存当前的后端
    current_backend = matplotlib.get_backend()
    
    # 设置为Agg后端
    matplotlib.use('Agg')
    
    # 创建一个字典，用于存储本地变量
    local_vars = {"plt": plt, "pd": pd, "sns": sns}
    
    try:
        exec(py_code, g, local_vars)
    except Exception as e:
        return f"代码执行时报错: {e}"
    finally:
        # 恢复默认后端
        matplotlib.use(current_backend)
    
    # 根据图片名称，获取图片对象
    fig = local_vars[fname]
    
    
    # 上传图片
    try:
        fig_url = upload_fig_to_oss(fig)
        markdown_text = f"![Image]({fig_url})"
        # display(Markdown(markdown_text))
        res = f"已经成功运行代码，并已将代码创建的图片存储至：{fig_url}"
        
    except Exception as e:
        res = "无法上传图片至阿里云oss，请检查相关设置"
        
    print(res)
    return res

# create_knowledge_base_folder(sub_folder_name=None)

def is_folder_not_empty(knowledge_base_name):
    
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')
    
    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')
    
    # 目标文件夹路径
    target_folder_path = os.path.join(base_path, knowledge_base_name)
    
    # 检查目标文件夹是否存在
    if not os.path.exists(target_folder_path) or not os.path.isdir(target_folder_path):
        print(f"目标文件夹 {target_folder_path} 不存在或不是一个文件夹。")
        return False
    
    # 遍历目标文件夹中的文件
    for root, dirs, files in os.walk(target_folder_path):
        for file in files:
            if not file.endswith('.json'):
                return True
    
    return False

def google_search(query, num_results=10, site_url=None):
    
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    cse_id = os.getenv("CSE_ID")
    
    url = "https://www.googleapis.com/customsearch/v1"

    # API 请求参数
    if site_url == None:
        params = {
        'q': query,          
        'key': api_key,      
        'cx': cse_id,        
        'num': num_results   
        }
    else:
        params = {
        'q': query,         
        'key': api_key,      
        'cx': cse_id,        
        'num': num_results,  
        'siteSearch': site_url
        }

    # 发送请求
    response = requests.get(url, params=params)
    response.raise_for_status()

    # 解析响应
    search_results = response.json().get('items', [])

    # 提取所需信息
    results = [{
        'title': item['title'],
        'link': item['link'],
        # 'snippet': item['snippet']
    } for item in search_results]

    return results

def windows_compatible_name(s, max_length=255):
    """
    将字符串转化为符合Windows文件/文件夹命名规范的名称。
    
    参数:
    - s (str): 输入的字符串。
    - max_length (int): 输出字符串的最大长度，默认为255。
    
    返回:
    - str: 一个可以安全用作Windows文件/文件夹名称的字符串。
    """

    # Windows文件/文件夹名称中不允许的字符列表
    forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    # 使用下划线替换不允许的字符
    for char in forbidden_chars:
        s = s.replace(char, '_')

    # 删除尾部的空格或点
    s = s.rstrip(' .')

    # 检查是否存在以下不允许被用于文档名称的关键词，如果有的话则替换为下划线
    reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", 
                      "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]
    if s.upper() in reserved_names:
        s += '_'

    # 如果字符串过长，进行截断
    if len(s) > max_length:
        s = s[:max_length]

    return s

def get_search_text(q, url):
    
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    cookie = os.getenv('ZHIHU_SEARCH_COOKIE')
    user_agent = os.getenv('ZHIHU_SEARCH_USER_AGENT')    
    title = None
    
    code_ = False
    headers = {
        'authority': 'www.zhihu.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'upgrade-insecure-requests': '1',
        'user-agent':user_agent,
    }

    # 普通问答地址
    if 'zhihu.com/question' in url:
        res = requests.get(url, headers=headers).text
        res_xpath = etree.HTML(res)
        title = res_xpath.xpath('//div/div[1]/div/h1/text()')[0]
        text_d = res_xpath.xpath('//div/div/div/div[2]/div/div[2]/div/div/div[2]/span[1]/div/div/span/p/text()')
    
    # 专栏地址
    elif 'zhuanlan' in url:
        headers['authority'] = 'zhaunlan.zhihu.com'
        res = requests.get(url, headers=headers).text
        res_xpath = etree.HTML(res)
        title = res_xpath.xpath('//div[1]/div/main/div/article/header/h1/text()')[0]
        text_d = res_xpath.xpath('//div/main/div/article/div[1]/div/div/div/p/text()')
        code_ = res_xpath.xpath('//div/main/div/article/div[1]/div/div/div//pre/code/text()')  
            
    # 特定回答的问答网址
    elif 'answer' in url:
        res = requests.get(url, headers=headers).text
        res_xpath = etree.HTML(res)
        title = res_xpath.xpath('//div/div[1]/div/h1/text()')[0]
        text_d = res_xpath.xpath('//div[1]/div/div[3]/div/div/div/div[2]/span[1]/div/div/span/p/text()')

    if title == None:
        return None
    
    else:
        title = windows_compatible_name(title)

        # 创建问题答案正文
        text = ''
        for t in text_d:
            txt = str(t).replace('\n', ' ')
            text += txt

        # 如果有code，则将code追加到正文的追后面
        if code_:
            for c in code_:
                co = str(c).replace('\n', ' ')    
                text += co

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")     
        json_data = [
            {
                "link": url,
                "title": title,
                "content": text,
                "tokens": len(encoding.encode(text))
            }
        ]

        path = create_knowledge_base_folder(sub_folder_name='auto_search')
        # 使用 os.path.join 构建文件路径
        file_path = os.path.join(path, q, f"{title}.json")

        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 打开文件并写入数据
        with open(file_path, 'w') as f:
            json.dump(json_data, f)

        return title

def get_answer(q, g='globals()'):
    """
    当你无法回答某个问题时，调用该函数，能够获得答案
    :param q: 必选参数，询问的问题，字符串类型对象
    :return：某问题的答案，以字符串形式呈现
    """
    # 调用转化函数，将用户的问题转化为更适合在知乎上进行搜索的关键词
    q = convert_keyword(q)
    
    # 默认搜索返回10个答案
    print('正在接入谷歌搜索，查找和问题相关的答案...')
    results = google_search(query=q, num_results=10, site_url='https://zhihu.com/')
    
    # 创建对应问题的子文件夹
    path = create_knowledge_base_folder(sub_folder_name='auto_search')
    folder_path = os.path.join(path, q)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    clear_folder(folder_path)
    
    # 单独提取links放在一个list中
    print('正在读取搜索的到的相关答案...')
    num_tokens = 0
    content = ''
    for item in results:
        url = item['link']
        title = get_search_text(q, url)
        file_path = os.path.join(folder_path, f"{title}.json")
        with open(file_path, 'r') as f:
            jd = json.load(f)
        num_tokens += jd[0]['tokens']
        if num_tokens <= 12000:
            content += jd[0]['content']
        else:
            break
    print('正在进行最后的整理...')
    return content

def get_search_text_github(q, dic, path):
    title = dic['owner'] + '_' + dic['repo']
    title = windows_compatible_name(title)

    # 创建问题答案正文
    text = get_github_readme(dic)

    # 写入本地json文件
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    json_data = [
        {
            "title": title,
            "content": text,
            "tokens": len(encoding.encode(text))
        }
    ]

    folder_path = os.path.join(path, q)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"{title}.json")
    with open(file_path, 'w') as f:
        json.dump(json_data, f)

    return title


def get_github_readme(dic):
    
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    github_token = os.getenv('GITHUB_TOKEN')
    user_agent = os.getenv('ZHIHU_SEARCH_USER_AGENT')
    
    owner = dic['owner']
    repo = dic['repo']

    headers = {
        "Authorization": github_token,
        "User-Agent": user_agent
    }

    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/readme", headers=headers)

    readme_data = response.json()
    encoded_content = readme_data.get('content', '')
    decoded_content = base64.b64decode(encoded_content).decode('utf-8')
    
    return decoded_content

def extract_github_repos(search_results):
    # 使用列表推导式筛选出项目主页链接
    repo_links = [result['link'] for result in search_results if '/issues/' not in result['link'] and '/blob/' not in result['link'] and 'github.com' in result['link'] and len(result['link'].split('/')) == 5]

    # 从筛选后的链接中提取owner和repo
    repos_info = [{'owner': link.split('/')[3], 'repo': link.split('/')[4]} for link in repo_links]

    return repos_info

def get_answer_github(q, g='globals()'):
    """
    当你无法回答某个问题时，调用该函数，能够获得答案
    :param q: 必选参数，询问的问题，字符串类型对象
    :return：某问题的答案，以字符串形式呈现
    """
    # 调用转化函数，将用户的问题转化为更适合在GitHub上搜索的关键词
    q = convert_keyword_github(q)
    
    # 默认搜索返回10个答案
    print('正在接入谷歌搜索，并在GitHub上搜索相关项目...')
    search_results = google_search(query=q, num_results=10, site_url='https://github.com/')
    results = extract_github_repos(search_results)
    
    # 创建对应问题的子文件夹
    path = create_knowledge_base_folder(sub_folder_name='auto_search')
    folder_path = os.path.join(path, q)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    clear_folder(folder_path)
    print('正在读取相关项目说明文档...')
    num_tokens = 0
    content = ''
    
    for dic in results:
        title = get_search_text_github(q, dic, path)
        file_path = os.path.join(folder_path, f"{title}.json")
        with open(file_path, 'r') as f:
            jd = json.load(f)
        num_tokens += jd[0]['tokens']
        if num_tokens <= 12000:
            content += jd[0]['content']
        else:
            break
    print('正在进行最后的整理...')
    return content
    
def get_vector_db_id(knowledge_base_name):
    # 获取 KNOWLEDGE_LIBRARY_PATH 环境变量
    knowledge_library_path = os.getenv('KNOWLEDGE_LIBRARY_PATH')
    
    # 检查 KNOWLEDGE_LIBRARY_PATH 是否存在且路径是否有效
    if knowledge_library_path and os.path.exists(knowledge_library_path):
        base_path = os.path.join(knowledge_library_path, 'knowledge_base')
    else:
        # 如果 KNOWLEDGE_LIBRARY_PATH 不存在或路径无效，则在 home 目录下创建文件夹
        home_dir = str(Path.home())
        base_path = os.path.join(home_dir, 'knowledge_base')
    
    # 检查主目录 JSON 文件
    main_json_file = os.path.join(base_path, 'main_vector_db_mapping.json')
    if not os.path.exists(main_json_file):
        print(f"{main_json_file} 不存在。")
        return None
    
    # 读取主目录 JSON 文件
    with open(main_json_file, 'r') as f:
        main_mapping = json.load(f)
    
    # 检索对应的词向量数据库ID
    vector_db_id = main_mapping.get(knowledge_base_name)
    
    return vector_db_id    

def wait_for_vector_store_ready(vs_id, client, interval=3, max_attempts=20):
    attempt = 0
    while attempt < max_attempts:
        vector_store = client.beta.vector_stores.retrieve(vs_id)
        if vector_store.status == 'completed':
            return True
        time.sleep(interval)
        attempt += 1
    return False    