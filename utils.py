from prompt_template import system_template_text,user_template_text, system_template_text_1, user_template_text_1
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from IncompleteText_model import IncompleteText
from CompleteText_model import CompleteText
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

import os
import streamlit as st

llm = AzureChatOpenAI(  # 获取模型
    deployment_name="agentlive-gpt4o",
    openai_api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_endpoint=st.secrets["general"]["AZURE_OPENAI_ENDPOINT"],
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    openai_api_key=st.secrets["general"]["AZURE_OPENAI_API_KEY"]
    # temperature=0,
    # max_tokens=1024,
    # request_timeout=60,
    # frequency_penalty=1.5
)

memory = ConversationBufferMemory(memory_key="history", return_messages=True)


def generate_incomplete_text(theme, wordnum):
    # 提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system",system_template_text),
        ("user",user_template_text)
    ])

    output_parser = PydanticOutputParser(pydantic_object=IncompleteText)        #输出解析器
    chain = prompt | llm | output_parser
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme,
        "wordnum": wordnum
    })
    memory.save_context({"input": theme}, {"output": result.text})
    return result


def generate_complete_text(input_filling):

    # 设置对话内存
    history = memory.load_memory_variables({})["history"]
    # 提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system",system_template_text_1),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user",user_template_text_1)
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

    #清空记忆
    # memory.clear()
    print(result.content)

    return result.content


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