import streamlit as st # Streamlit 是最快落地交易看板的选择

def show_dashboard():
    st.set_page_config(layout="wide")
    st.title("A股极速交易中台 - 实时概览")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("核心链路延迟", "156 μs", "-2μs")
    with col2:
        st.metric("当日成交额", "¥ 1,245,000", "+5%")
    with col3:
        st.metric("策略健康度", "99.9%", "Stable")

    st.subheader("实时策略流水")
    # 这里可以读取 Redis 列表展示最新订单
    st.table([
        {"时间": "10:30:01", "代码": "600519", "动作": "买入", "状态": "完全成交"},
        {"时间": "10:31:45", "代码": "000001", "动作": "卖出", "状态": "已报单"}
    ])

if __name__ == "__main__":
    show_dashboard()