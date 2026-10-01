"""
TrafficAgent: 交通分析與優化評估代理人 (具備六階段推理架構與 ChatLogger 整合)
"""

from typing import Dict, Any, List, Optional
from src.chat_logger import ChatLogger


class TrafficAgent:
    """處理交通模擬與號誌優化諮詢之智慧代理人。"""

    def __init__(self, logger: Optional[ChatLogger] = None):
        self.logger = logger or ChatLogger()

    def process_query(
        self,
        user_query: str,
        intersection_name: str = "中正路與復興路口",
        time_period: str = "上午尖峰 (07:30 - 08:30)",
        alpha: float = 0.35,
        dedicated_left_turn_lane: bool = True
    ) -> Dict[str, Any]:
        """執行六階段推理並呼叫 ChatLogger 記錄互動過程。"""

        # 1. Understand（理解需求）
        stage_understand = (
            f"接收使用者對路口『{intersection_name}』在『{time_period}』之交通諮詢。\n"
            f"使用者關切焦點：{user_query}\n"
            f"設定參數：機車分流比例 alpha={alpha}，配置左轉專用道={dedicated_left_turn_lane}。"
        )

        # 2. Plan & Reason（規劃推理）
        stage_plan = (
            "規劃推理路徑：\n"
            "1. 檢索歷史車流資料庫與各車道轉向衝突點 (Turn Conflict Matrix)。\n"
            "2. 評估現行號誌週期與內側車道直行/左轉混合造成的延滯。\n"
            "3. 藉由分流係數 alpha 計算消除直行與左轉衝突後之路口服務水準 (LOS) 提升潛力。\n"
            "4. 驗證是否符合交通法規對於偏心左轉專用道與早開時相之設置標準。"
        )

        # 3. Data Acquisition（取得資料）
        stage_acquisition = (
            f"模擬擷取路口偵測器數據與歷史調查量：\n"
            f"- 總通過車流量：2,480 PCU/hr（機車佔比約 48%）\n"
            f"- 內側車道直左混合衝突率：約 28.4%\n"
            f"- 平均停等延滯時間（未改善前）：58.6 秒/車 (LOS E)"
        )

        # 4. Analyze（資料分析）
        improved_delay = round(58.6 * (1 - alpha * 0.45) - (8.5 if dedicated_left_turn_lane else 0), 1)
        improved_los = "C" if improved_delay < 35 else ("D" if improved_delay < 55 else "E")
        stage_analyze = (
            f"運算分析結果：\n"
            f"- 內側車道機車分流係數 alpha={alpha} 導入後，左轉與直行剪刀衝突降低約 {round(alpha * 100, 1)}%。\n"
            f"- 停等延滯時間由 58.6 秒降至 {improved_delay} 秒/車。\n"
            f"- 路口服務水準由 LOS E 改善為 LOS {improved_los}。\n"
            f"- 設置專用左轉道之效益加乘：顯著改善防禦性轉向視野與縮短清道時間。"
        )

        # 5. Generate（生成建議）
        stage_generate = (
            "整合推論並產出工程建議報告：\n"
            "1. 建議實施路口實體或標線型偏心左轉專用車道。\n"
            "2. 搭配早開/遲閉左轉保護時相，分離直行與左轉車流。\n"
            "3. 配合內側車道合理分流管制，降低機車外側鬼切左轉風險。"
        )

        # 6. Interact（互動呈現）
        stage_interact = (
            "將運算數據與建議轉換為易於閱讀之結構化摘要，並標註法規條文依據供決策參考。"
        )

        stages = {
            "Understand": stage_understand,
            "Plan & Reason": stage_plan,
            "Data Acquisition": stage_acquisition,
            "Analyze": stage_analyze,
            "Generate": stage_generate,
            "Interact": stage_interact
        }

        agent_response = (
            f"針對【{intersection_name}】在【{time_period}】的交通優化評估：\n\n"
            f"1. **評估成果摘要**：\n"
            f"   - 當前模擬內側分流比率為 `{alpha}`，搭配左轉專用道配置。\n"
            f"   - 預估平均延滯時間可由 `58.6 秒` 改善至 `{improved_delay} 秒`，服務水準提升至 **LOS {improved_los}**。\n"
            f"   - 直左衝突點減少達 `{round(alpha * 100, 1)}%`，大幅降低路口交織事故風險。\n\n"
            f"2. **改善工程配套建議**：\n"
            f"   - 削設中央分隔島增設偏心左轉專用車道，避免左轉待轉車阻斷內側直行車流。\n"
            f"   - 號誌週期調整為多時相管制（左轉保護早開時相）。"
        )

        citations = [
            "《道路交通標誌標線號誌設置規則》第65條（左轉專用號誌時相之設置標準）",
            "《道路交通標誌標線號誌設置規則》第183條之1（偏心左轉專用車道設置原則）"
        ]

        # 記錄至 ChatLogger
        self.logger.log_interaction(
            intersection_name=intersection_name,
            time_period=time_period,
            alpha=alpha,
            dedicated_left_turn_lane=dedicated_left_turn_lane,
            user_query=user_query,
            agent_thought_stages=stages,
            agent_response=agent_response,
            citations=citations
        )

        return {
            "response": agent_response,
            "thought_stages": stages,
            "citations": citations,
            "metrics": {
                "before_delay": 58.6,
                "after_delay": improved_delay,
                "improved_los": improved_los
            }
        }
