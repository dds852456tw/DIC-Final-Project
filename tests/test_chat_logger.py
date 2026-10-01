"""
Tests for ChatLogger:
1. 驗證呼叫 ChatLogger.log_interaction 後，chatLog.md 成功建立且非空白。
2. 驗證連續發送兩次不同時段提問時，採用追加寫入（Append）而非覆蓋舊紀錄（兩筆提問與時間戳記皆存在）。
3. 驗證寫入的 Markdown 完整包含使用者問題、六階段關鍵字（Understand 至 Interact）與最終評估報告。
"""

import os
import pytest
from src.chat_logger import ChatLogger
from src.traffic_agent import TrafficAgent


@pytest.fixture
def temp_log_file(tmp_path):
    """建立測試用臨時 log 檔案路徑。"""
    log_file = tmp_path / "test_chatLog.md"
    return str(log_file)


def test_chat_logger_creates_file_and_not_empty(temp_log_file):
    """測試呼叫 ChatLogger.log_interaction 後，檔案成功建立且非空白。"""
    logger = ChatLogger(log_path=temp_log_file)
    assert not os.path.exists(temp_log_file)

    agent = TrafficAgent(logger=logger)
    result = agent.process_query(
        user_query="測試路口交通流量與延滯時間",
        intersection_name="中正路與復興路口",
        time_period="上午尖峰 (07:30 - 08:30)",
        alpha=0.3,
        dedicated_left_turn_lane=True
    )

    assert os.path.exists(temp_log_file)
    content = logger.read_log()
    assert len(content.strip()) > 0
    assert "中正路與復興路口" in content
    assert "測試路口交通流量與延滯時間" in content


def test_chat_logger_appends_multiple_interactions(temp_log_file):
    """測試連續發送兩次不同時段提問時，採用 Append 模式而非覆蓋舊紀錄。"""
    logger = ChatLogger(log_path=temp_log_file)
    agent = TrafficAgent(logger=logger)

    # 第一次提問：上午尖峰
    agent.process_query(
        user_query="上午尖峰如何改善延滯？",
        intersection_name="中正路與復興路口",
        time_period="上午尖峰 (07:30 - 08:30)",
        alpha=0.35,
        dedicated_left_turn_lane=True
    )

    # 第二次提問：下午尖峰
    agent.process_query(
        user_query="下午尖峰車流大增，左轉回堵情況如何緩解？",
        intersection_name="民生路與中山路口",
        time_period="下午尖峰 (17:30 - 18:30)",
        alpha=0.45,
        dedicated_left_turn_lane=False
    )

    content = logger.read_log()

    # 驗證兩筆提問皆完整保留
    assert "上午尖峰如何改善延滯？" in content
    assert "下午尖峰車流大增，左轉回堵情況如何緩解？" in content

    # 驗證兩筆路口與時段皆存在
    assert "中正路與復興路口" in content
    assert "民生路與中山路口" in content
    assert "上午尖峰 (07:30 - 08:30)" in content
    assert "下午尖峰 (17:30 - 18:30)" in content

    # 驗證至少包含兩組系統互動紀錄標題
    count_headers = content.count("【專題系統對話與六階段推理記錄（System Runtime Chat Logger）】")
    assert count_headers == 2


def test_chat_logger_contains_six_stages_and_report(temp_log_file):
    """測試寫入之 Markdown 內容是否完整包含使用者問題、六階段關鍵字與最終評估報告。"""
    logger = ChatLogger(log_path=temp_log_file)
    agent = TrafficAgent(logger=logger)

    query = "請問提高機車內側車道行駛比率對路口安全有何影響？"
    agent.process_query(
        user_query=query,
        intersection_name="中華路與和平路口",
        time_period="離峰時段 (13:30 - 14:30)",
        alpha=0.4,
        dedicated_left_turn_lane=True
    )

    content = logger.read_log()

    # 驗證使用者問題
    assert query in content

    # 驗證六階段推理關鍵字
    six_stages = [
        "Understand",
        "Plan & Reason",
        "Data Acquisition",
        "Analyze",
        "Generate",
        "Interact"
    ]
    for stage in six_stages:
        assert stage in content, f"Missing stage keyword: {stage}"

    # 驗證包含最終評估報告關鍵標題與法規依據
    assert "AI 代理人最終回覆與法規依據" in content
    assert "道路交通標誌標線號誌設置規則" in content
