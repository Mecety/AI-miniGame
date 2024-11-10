from prompt_template import system_template_text, user_template_text, system_template_text_1, user_template_text_1
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from IncompleteText_model import IncompleteText
from CompleteText_model import CompleteText
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from sqlalchemy import create_engine, text

import os
import streamlit as st
import sqlite3
llm = AzureChatOpenAI(  # 获取模型
    deployment_name="agentlive-gpt4o",
    openai_api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    # azure_endpoint=st.secrets["general"]["AZURE_OPENAI_ENDPOINT"],
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    # openai_api_key=st.secrets["general"]["AZURE_OPENAI_API_KEY"]
    # temperature=0,
    # max_tokens=1024,
    # request_timeout=60,
    # frequency_penalty=1.5
)

# 设置对话内存
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# 创建连接池
engine = create_engine('sqlite:///chat_memory.db', pool_size=5, max_overflow=10)

def generate_incomplete_text(theme, wordnum):
    # 提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text),
        ("user", user_template_text)
    ])

    output_parser = PydanticOutputParser(pydantic_object=IncompleteText)  # 输出解析器
    chain = prompt | llm | output_parser
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme,
        "wordnum": wordnum
    })

    # 从连接池获取连接并执行数据库操作
    with engine.connect() as conn:
        conn.execute(text('INSERT INTO chat_history (theme, wordnum, result) VALUES (:theme, :wordnum, :result)'),
                     {"theme": theme, "wordnum": wordnum, "result": result.text})

    # 保存到内存
    memory.save_context({"input": theme}, {"output": result.text})
    
    return result

def generate_complete_text(input_filling):
    # 从内存中加载当前对话历史
    history = memory.load_memory_variables({})["history"]

    # 从连接池获取连接并加载最新一行的对话历史
    with engine.connect() as conn:
        result = conn.execute(text('SELECT theme, wordnum, result FROM chat_history ORDER BY id DESC LIMIT 1'))
        row = result.fetchone()

    # 检查是否有结果
    if row:
        latest_history = {"theme": row['theme'], "wordnum": row['wordnum'], "result": row['result']}
        # 将最新的历史添加到 history 列表中
        history.append(latest_history)
    else:
        latest_history = None  # 如果没有数据，返回 None 或其他默认值

    # 提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text_1),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", user_template_text_1)
    ])
    # 输出解析器
    output_parser = PydanticOutputParser(pydantic_object=CompleteText)
    # 初始化 ConversationChain
    chain = prompt | llm

    result = chain.invoke({
        'chat_history': history,
        # "parser_instructions": output_parser.get_format_instructions(),
        "input_filling": input_filling
    })

    
    # print(result.content)

    return result.content

def clear_memory():
    """清空对话内存"""
    memory.clear()

# 在应用关闭时关闭数据库连接
def close_connection():
    # SQLAlchemy 的连接池会自动管理连接的关闭
    pass

# 确保在应用关闭时调用 close_connection()
# print(generate_incomplete_text("飞行", 50))
# result = generate_complete_text("小猫")
# print(result)
#
# try:
#     data_dict = json.loads(result)
#     print(data_dict)
# except json.JSONDecodeError as e:
#     print(f"JSON decode error: {e}")
#     print(f"Invalid JSON: '{result}'")


# complete_text_1 = data_dict["completeText1"]
# complete_text_2 = data_dict["completeText2"]
# print(complete_text_1)
