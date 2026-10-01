"""
ChatLogger: 全程對話與推理日誌自動記錄機制 (Chat & Workflow Logger)
支援開發過程記錄 (Antigravity Development Log) 與專題系統六階段推理記錄 (System Runtime Chat Logger)。
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional, List


class ChatLogger:
    """負責將開發紀錄與系統對話/六階段推理紀錄追加寫入 Markdown 檔案。"""

    def __init__(self, log_path: str = "chatLog.md"):
        self.log_path = log_path

    def _ensure_file_exists(self):
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write("# 🚦 專案全程對話與推理日誌 (Chat & Workflow Logger)\n\n")
                f.write("> 本檔案由系統自動記錄，包含開發過程日誌（Antigravity Development Log）與系統執行期六階段推理紀錄（System Runtime Chat Logger）。\n\n---\n\n")

    def log_development_step(
        self,
        prompt: str,
        execution_plan: str,
        modified_files: List[str],
        pytest_summary: str,
        timestamp: Optional[str] = None
    ) -> None:
        """記錄 Antigravity 開發過程（Prompt、執行計畫、修改檔案清單、pytest 結果）。"""
        self._ensure_file_exists()
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        files_str = "\n".join([f"- `{f}`" for f in modified_files]) if modified_files else "- 無修改檔案"

        entry = f"""## 🛠️ 【開發過程紀錄（Antigravity Development Log）】
- **記錄時間**：`{timestamp}`
- **階段類型**：開發過程紀錄

### 📥 使用者需求（User Prompt）
```text
{prompt.strip()}
```

### 📋 執行計畫（Execution Plan）
{execution_plan.strip()}

### 📁 修改檔案清單（Modified Files）
{files_str}

### 🧪 測試結果摘要（Pytest Summary）
```text
{pytest_summary.strip()}
```

---

"""
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    def log_interaction(
        self,
        intersection_name: str,
        time_period: str,
        alpha: float,
        dedicated_left_turn_lane: bool,
        user_query: str,
        agent_thought_stages: Dict[str, Any],
        agent_response: str,
        citations: Optional[List[str]] = None,
        timestamp: Optional[str] = None
    ) -> None:
        """記錄專題系統對話與六階段推理軌跡。
        agent_thought_stages 需涵蓋：
        - Understand（理解需求）
        - Plan & Reason（規劃推理）
        - Data Acquisition（取得資料）
        - Analyze（資料分析）
        - Generate（生成建議）
        - Interact（互動呈現）
        """
        self._ensure_file_exists()
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        citations_list = citations if citations else [
            "《道路交通標誌標線號誌設置規則》第65條（左轉專用時相設置依據）",
            "《道路交通標誌標線號誌設置規則》第183條之1（停等區與偏心左轉車道劃設原則）"
        ]
        citations_str = "\n".join([f"- 📜 {c}" for c in citations_list])

        # 格式化六階段思考軌跡
        stages_order = [
            ("Understand", "理解需求"),
            ("Plan & Reason", "規劃推理"),
            ("Data Acquisition", "取得資料"),
            ("Analyze", "資料分析"),
            ("Generate", "生成建議"),
            ("Interact", "互動呈現")
        ]

        stage_blocks = []
        for key, name_zh in stages_order:
            val = agent_thought_stages.get(key) or agent_thought_stages.get(f"{key}（{name_zh}）") or "無詳細紀錄"
            stage_blocks.append(f"#### 🔹 Stage: {key}（{name_zh}）\n{val.strip()}\n")

        thought_log_str = "\n".join(stage_blocks)

        entry = f"""## 🚦 【專題系統對話與六階段推理記錄（System Runtime Chat Logger）】
- **紀錄時間（Timestamp）**：`{timestamp}`
- **階段類型（Record Type）**：系統互動紀錄

### 📍 路口與環境參數（Environment Parameters）
| 參數名稱 | 數值 / 設定 |
| :--- | :--- |
| **目標路口名稱** | `{intersection_name}` |
| **分析時段（time_period）** | `{time_period}` |
| **模擬內側分流比例（alpha）** | `{alpha}` |
| **啟用左轉專用道配套** | `{'是 (True)' if dedicated_left_turn_lane else '否 (False)'}` |

### 💬 使用者輸入（User Query）
> {user_query}

### 🧠 代理人六階段思考軌跡（Agent 6-Stage Thought Log）
> 完整軌跡：`Understand（理解需求） -> Plan & Reason（規劃推理） -> Data Acquisition（取得資料） -> Analyze（資料分析） -> Generate（生成建議） -> Interact（互動呈現）`

{thought_log_str}

### 🤖 AI 代理人最終回覆與法規依據（Agent Response & Citations）
#### 📝 評估報告：
{agent_response.strip()}

#### 📚 引用法規依據：
{citations_str}

---

"""
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    def read_log(self) -> str:
        """讀取當前日誌內容，若檔案不存在則回傳空字串。"""
        if not os.path.exists(self.log_path):
            return ""
        with open(self.log_path, "r", encoding="utf-8") as f:
            return f.read()
