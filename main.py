import streamlit as st
import json
from utils import generate_incomplete_text,generate_complete_text

# 设置页面标题
st.title("我的应用程序")

# 创建一个漂亮的 HUD
st.sidebar.title("导航")
st.sidebar.markdown("---")  # 添加分隔线

# 定义页面状态
if "page" not in st.session_state:
    st.session_state.page = "主页"

# 创建自定义按钮
def create_button(label):
    if st.sidebar.button(label):
        st.session_state.page = label

# 创建可点击的页面按钮
create_button("主页")
create_button("页面 1")
create_button("页面 2")

# 根据选择的页面显示不同的内容
if st.session_state.page == "主页":
    st.header("欢迎来到主页")
    st.write("欢迎来到AI小游戏！在这里，你可以体验各种有趣的AI生成故事。选择一个主题，开始你的创作之旅吧！")
elif st.session_state.page == "页面 1":



    st.header("故事完形填空")

    option = st.selectbox("主题", ["随机", "自定义"])
    wordsnum = st.selectbox("文本字数", [50, 100, 200, 300, 400])

    if option == "自定义":
        theme = st.text_input("故事主题")

    if "submitButton_disabled" not in st.session_state:
        st.session_state.submitButton_disabled = False

    submit = st.button("生成文本", disabled=st.session_state.submitButton_disabled)

    if submit:
        st.session_state.submitButton_disabled = True
        
        if option == "自定义" and not theme:
            st.info("请输入故事主题或者选择随机生成")
            st.stop()

        if option == "随机":
            theme = "随机主题"

        with st.spinner("AI正在努力创作中，请稍等..."):
            result = generate_incomplete_text(theme, wordsnum)

        st.session_state['result'] = result
        st.session_state['inputs'] = [''] * result.blank_num
        st.rerun()


    # 获取之前生成的结果
    if 'result' in st.session_state:
        result = st.session_state['result']

        st.divider()
        left_column, right_column = st.columns(2)
        with left_column:
            st.write(result.text)
        with right_column:
            with st.form(key="input_form"):
                # 显示输入框
                for i in range(result.blank_num):
                    user_input = st.text_input(f"输入框 {i + 1}", key=f"input_{i}", value=st.session_state['inputs'][i])
                    st.session_state['inputs'][i] = user_input  # 更新session_state中的输入值

                # 提交按钮
                if "submitButton1_disabled" not in st.session_state:
                    st.session_state.submitButton1_disabled = False
                submit_1 = st.form_submit_button("提交", disabled=st.session_state.submitButton1_disabled)

                # 当点击提交按钮后，显示所有输入框的值
            if submit_1:
                # 立即更新按钮状态
                st.session_state.submitButton1_disabled = True


                with st.spinner("AI正在努力创作中，请稍等..."):
                    completeText = generate_complete_text(st.session_state['inputs'])

                # 更新结果
                st.session_state['completeText'] = completeText
                st.rerun()

    # 获取之前生成的完整文本
    if 'completeText' in st.session_state:
        # 调试输出，确认状态存在
        print("completeText 存在:", st.session_state['completeText'])

        data_dict = {}
        completeText = st.session_state['completeText']
        try:
            # 调试输出，确认JSON内容
            print("尝试解析JSON:", completeText)
            data_dict = json.loads(completeText)
            print("JSON 解析成功:", data_dict)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print("无效的JSON内容:", completeText)
            data_dict = {"completeText1": "无效文本", "completeText2": "无效文本"}  # 设置默认值以防出错

        complete_text_1 = data_dict["completeText1"]
        complete_text_2 = data_dict["completeText2"]
        print("完整文本1:", complete_text_1)
        print("完整文本2:", complete_text_2)
        # try:
        #     complete_text_1 = data_dict["completeText1"]
        #     complete_text_2 = data_dict["completeText2"]
        # except KeyError as e:
        #     print(f"JSON decode error: {e}")
        #     print(f"Invalid JSON: '{result}'")
        st.divider()
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown("##### 补全后文本")
            st.write(complete_text_1)
        with right_column:
            st.markdown("##### 改写后文本")
            st.write(complete_text_2)

        # 再玩一次按钮
        rerun = st.button("再玩一次")
        if rerun:
           # 保持在页面 1
            st.session_state.page = "页面 1"
            # 重置与游戏相关的状态
            st.session_state.submitButton_disabled = False
            st.session_state.submitButton1_disabled = False
            st.session_state.pop('result', None)
            st.session_state.pop('completeText', None)
            st.session_state.pop('inputs', None)
            st.session_state.page = "页面 1"
            st.rerun()







elif st.session_state.page == "页面 2":
    st.header("页面 2")
    st.write("这是页面 2 的内容。这里可以放置图表或其他可视化元素。")