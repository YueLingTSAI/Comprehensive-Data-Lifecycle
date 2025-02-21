import re
import logging
from typing import Dict, List, Tuple, Any
from google.cloud import language_v1

class SentimentAnalyzer:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()
        self.logger = logging.getLogger(__name__)
        
    def analyze_text_sentiment(self, text: str) -> Tuple[float, float]:
        """分析文本的情感，回傳 (情感分數, 情感強度)"""
        try:
            if not text or not text.strip():
                return 0.0, 0.0
                
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language='zh-TW'
            )
            
            sentiment = self.client.analyze_sentiment(
                request={'document': document}
            ).document_sentiment
            
            return sentiment.score, sentiment.magnitude
            
        except Exception as e:
            self.logger.error(f"分析文本情感時發生錯誤: {str(e)}")
            return 0.0, 0.0
            
    def calculate_sentiment(self, record: Dict[str, Any]) -> Tuple[str, int]:
        """計算加權情感分數和對應的情感標籤"""
        try:
            # 獲取原始文本以進行特殊詞彙檢測
            raw_text = record.get('content_text', '').lower()
            primary_target = record.get('keyword', '').strip().lower()
            is_comparison = record.get('is_comparison', False)
            compared_shops = record.get('compared_shops', [])
            
            # 特殊比較處理
            if is_comparison:
                sentiment_score = self._handle_comparison(raw_text, primary_target, compared_shops)
                if sentiment_score is not None:
                    normalized_score = 3 + (sentiment_score * 2)
                    final_score = int(round(max(1, min(5, normalized_score))))
                    sentiment_levels = {
                        5: '強烈正面',
                        4: '正面',
                        3: '中性',
                        2: '負面',
                        1: '強烈負面'
                    }
                    return sentiment_levels[final_score], final_score
            
            # 檢測特殊情感模式
            comparison_patterns = [
                (r'比.+好喝', 0.7),
                (r'比.+難喝', -0.7),
                (r'屌打|完勝|秒殺|吊打', 0.8),
                (r'被屌打|被完勝|被秒殺', -0.8),
                (r'沒比較|不比|不如', -0.2),
                (r'太少|太慢|不夠', -0.3),
                (r'好喝多了|超好喝', 0.8),
                (r'難喝', -0.7),
                (r'貴又', -0.6),
                (r'只喝', 0.6)
            ]
            
            # 加權計算 (content_text 95%, article_title 3%, keyword 2%)
            base_weighted_score = (
                record.get('content_sentiment', 0) * 0.95 +
                record.get('title_sentiment', 0) * 0.03 +
                record.get('keyword_sentiment', 0) * 0.02
            )
            
            # 檢查特殊模式
            for pattern, score_adj in comparison_patterns:
                if re.search(pattern, raw_text):
                    # 根據模式調整分數
                    if (score_adj > 0 and base_weighted_score < 0) or (score_adj < 0 and base_weighted_score > 0):
                        base_weighted_score = score_adj
                    else:
                        base_weighted_score += (score_adj * 0.5)
                    break
            
            # 確保分數在 -1 到 1 的範圍內
            weighted_score = max(min(base_weighted_score, 1), -1)
            
            # 轉換到 1-5 分數範圍
            normalized_score = 3 + (weighted_score * 2)
            final_score = int(round(max(1, min(5, normalized_score))))
            
            sentiment_levels = {
                5: '強烈正面',
                4: '正面',
                3: '中性',
                2: '負面',
                1: '強烈負面'
            }
            
            return sentiment_levels[final_score], final_score
                
        except Exception as e:
            self.logger.error(f"計算情感分數時發生錯誤: {str(e)}")
            return '中性', 3
            
    def _handle_comparison(self, text: str, primary_target: str, compared_shops: List[str]) -> float:
        """處理比較類評論"""
        # 檢測是否有比較表達
        comparison_patterns = [
            (r'比.+好喝', 0.7),
            (r'屌打|完勝|秒殺|吊打', 0.8),
            (r'比.+難喝', -0.7),
            (r'不如|遜色|差很多', -0.5)
        ]
        
        # 確定比較的方向
        if primary_target == 'cama' and '路易莎' in compared_shops:
            # 檢查是 CAMA 比路易莎好，還是路易莎比 CAMA 好
            for pattern, score_adj in comparison_patterns:
                if re.search(rf'cama.{{0,20}}{pattern}.{{0,20}}路易莎', text, re.IGNORECASE):
                    # CAMA 比路易莎好
                    return 0.8 if score_adj > 0 else -0.8
                elif re.search(rf'路易莎.{{0,20}}{pattern}.{{0,20}}cama', text, re.IGNORECASE):
                    # 路易莎比 CAMA 好
                    return -0.8 if score_adj > 0 else 0.8
        
        elif primary_target == '路易莎' and 'cama' in compared_shops:
            # 檢查是路易莎比 CAMA 好，還是 CAMA 比路易莎好
            for pattern, score_adj in comparison_patterns:
                if re.search(rf'路易莎.{{0,20}}{pattern}.{{0,20}}cama', text, re.IGNORECASE):
                    # 路易莎比 CAMA 好
                    return 0.8 if score_adj > 0 else -0.8
                elif re.search(rf'cama.{{0,20}}{pattern}.{{0,20}}路易莎', text, re.IGNORECASE):
                    # CAMA 比路易莎好
                    return -0.8 if score_adj > 0 else 0.8
        
        return None