"""
Streamlit Web App: 交通分析與號誌評估系統 (含 Chat & Workflow Logger 線上檢視與下載功能)
"""

import streamlit as st
import os
from src.traffic_agent import TrafficAgent
from src.chat_logger import ChatLogger

st.set_page_config(
    page_title="智慧交通號誌與分流決策代理人",
    page_icon="🚦",
    layout="wide"
)

# 初始化日誌器與代理人
logger = ChatLogger(log_path="chatLog.md")
agent = TrafficAgent(logger=logger)

# 標題與簡介
st.title("🚦 智慧交通號誌與分流決策代理人 (AI Traffic Agent)")
st.caption("基於六階段推理架構 (Understand -> Plan -> Acquisition -> Analyze -> Generate -> Interact) 與即時日誌紀錄")

# 側邊欄：環境參數與日誌管理
with st.sidebar:
    st.header("⚙️ 模擬環境參數設定")
    intersection = st.selectbox(
        "目標路口名稱",
        ["中正路與復興路口", "民生路與中山路口", "中華路與和平路口", "八德路與光復路口"]
    )
    time_period = st.selectbox(
        "分析時段 (time_period)",
        ["上午尖峰 (07:30 - 08:30)", "下午尖峰 (17:30 - 18:30)", "離峰時段 (13:30 - 14:30)"]
    )
    alpha = st.slider(
        "模擬內側分流比例 (alpha)",
        min_value=0.0,
        max_value=0.8,
        value=0.35,
        step=0.05,
        help="機車或特定流向導入內側車道/分流之比率"
    )
    dedicated_left_lane = st.checkbox(
        "啟用偏心左轉專用道配套",
        value=True,
        help="依據標誌標線規則設置偏心左轉車道與左轉保護時相"
    )

    st.markdown("---")
    st.header("📄 對話與推理日誌 (chatLog.md)")
    
    # 讀取目前 chatLog.md 內容
    log_content = logger.read_log()
    
    st.download_button(
        label="📥 下載 chatLog.md 完整對話紀錄",
        data=log_content if log_content else "尚無紀錄",
        file_name="chatLog.md",
        mime="text/markdown",
        use_container_width=True
    )
    
    with st.expander("👀 線上預覽 chatLog.md (前 1500 字元)", expanded=False):
        if log_content:
            st.markdown(log_content[:1500] + ("\n\n*(以下省略，請下載查看完整檔案)*" if len(log_content) > 1500 else ""))
        else:
            st.info("目前尚無日誌記錄。")

# 主要區域：對話與提問
st.subheader("💬 智慧交通諮詢提問")
default_query = "目前路口內側車道直行與左轉車流交織嚴重，若提高分流比例並設置偏心左轉道，對路口延滯與服務水準有何改善？"
user_query = st.text_area("請輸入您的交通諮詢需求或問題：", value=default_query, height=90)

col_run, col_clear = st.columns([1, 5])
with col_run:
    submit_btn = st.button("🚀 執行代理人分析", type="primary", use_container_width=True)

if submit_btn and user_query.strip():
    with st.spinner("AI 代理人正在進行六階段推理分析中..."):
        result = agent.process_query(
            user_query=user_query,
            intersection_name=intersection,
            time_period=time_period,
            alpha=alpha,
            dedicated_left_turn_lane=dedicated_left_lane
        )
    
    st.success("✅ 推理與分析完成！已即時追加寫入 `chatLog.md`。")

    # 成果展示
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    col_metric1.metric("改善前平均延滯", f"{result['metrics']['before_delay']} 秒/車", delta="-LOS E", delta_color="inverse")
    col_metric2.metric("改善後預估延滯", f"{result['metrics']['after_delay']} 秒/車", delta=f"-{round(result['metrics']['before_delay'] - result['metrics']['after_delay'], 1)} 秒")
    col_metric3.metric("路口服務水準提升", f"LOS {result['metrics']['improved_los']}")

    # 代理人最終回覆
    st.markdown("### 📝 AI 代理人最終評估報告")
    st.markdown(result["response"])

    # 引用法規
    st.markdown("#### 📚 依循法規條文依據：")
    for cit in result["citations"]:
        st.markdown(f"- 📜 {cit}")

    # 六階段推理展開詳情
    with st.expander("🧠 檢視代理人六階段思考軌跡 (6-Stage Thought Log)", expanded=True):
        stages = result["thought_stages"]
        stage_names = [
            ("Understand", "理解需求"),
            ("Plan & Reason", "規劃推理"),
            ("Data Acquisition", "取得資料"),
            ("Analyze", "資料分析"),
            ("Generate", "生成建議"),
            ("Interact", "互動呈現")
        ]
        for en, zh in stage_names:
            st.markdown(f"**🔹 {en}（{zh}）**")
            st.text(stages[en])
            st.divider()

# 頁尾說明
st.markdown("---")
st.caption("本系統所有提問與推理步驟皆自動且即時持久化於專案根目錄之 `chatLog.md`。")
