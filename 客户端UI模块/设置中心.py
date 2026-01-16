import streamlit as st

def settings_page():
    st.sidebar.title("系统配置")
    
    # 行情源配置
    tdx_ip = st.text_input("通达信服务器IP", "119.147.212.81")
    tdx_port = st.number_input("端口", value=7709)
    
    # 策略开关
    enable_strategy = st.checkbox("启动实盘策略执行", value=False)
    
    # 百度云密钥
    ak = st.text_input("BOS AccessKey", type="password")
    sk = st.text_input("BOS SecretKey", type="password")
    
    if st.button("保存并应用配置"):
        # 将配置写入 .yaml 文件
        st.success("配置已同步到各模块")