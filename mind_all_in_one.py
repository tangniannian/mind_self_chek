import streamlit as st
import pandas as pd
import altair as alt
from pyvis.network import Network
import tempfile

st.set_page_config(page_title="思维导图工具", layout="wide")
st.title("简易思维导图生成器")

# 初始化数据
if "nodes" not in st.session_state:
    st.session_state.nodes = [{"id": 1, "name": "中心主题", "group": 0}]
if "edges" not in st.session_state:
    st.session_state.edges = []

# 侧边栏添加节点
st.sidebar.header("添加节点")
parent_id = st.sidebar.selectbox("选择父节点", [n["id"] for n in st.session_state.nodes], format_func=lambda x: [n["name"] for n in st.session_state.nodes if n["id"]==x][0])
new_name = st.sidebar.text_input("节点名称")
if st.sidebar.button("添加子节点") and new_name.strip():
    new_id = max([n["id"] for n in st.session_state.nodes]) + 1
    parent_node = [n for n in st.session_state.nodes if n["id"] == parent_id][0]
    st.session_state.nodes.append({"id": new_id, "name": new_name, "group": parent_node["group"]+1})
    st.session_state.edges.append({"from": parent_id, "to": new_id})
    st.rerun()

# 展示表格
col1, col2 = st.columns([1,2])
with col1:
    st.subheader("节点列表")
    df_node = pd.DataFrame(st.session_state.nodes)
    st.dataframe(df_node, use_container_width=True)

    st.subheader("连线关系")
    df_edge = pd.DataFrame(st.session_state.edges)
    st.dataframe(df_edge, use_container_width=True)

with col2:
    st.subheader("思维导图预览")
    net = Network(height="600px", width="100%", directed=True, bgcolor="#222222", font_color="white")
    for n in st.session_state.nodes:
        net.add_node(n["id"], label=n["name"], group=n["group"])
    for e in st.session_state.edges:
        net.add_edge(e["from"], e["to"])

    # 临时html文件展示
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as f:
        net.write_html(f.name)
        st.components.v1.html(open(f.name,"r",encoding="utf-8").read(), height=620)

# 清空
if st.button("清空全部"):
    st.session_state.nodes = [{"id": 1, "name": "中心主题", "group": 0}]
    st.session_state.edges = []
    st.rerun()
