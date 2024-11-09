import streamlit as st

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
    st.write("这是主页的内容。可以在这里放置一些简介信息。")
elif st.session_state.page == "页面 1":
    st.header("页面 1")
    st.write("这是页面 1 的内容。这里可以展示一些数据分析。")
elif st.session_state.page == "页面 2":
    st.header("页面 2")
    st.write("这是页面 2 的内容。这里可以放置图表或其他可视化元素。")
