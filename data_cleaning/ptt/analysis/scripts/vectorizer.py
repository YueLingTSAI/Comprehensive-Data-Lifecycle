import logging
from typing import List, Dict, Any, Tuple
import re
from .text_processor import TextProcessor
from .sentiment_analyzer import SentimentAnalyzer
from .topic_classifier import TopicClassifier

class TextVectorizer:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.topic_classifier = TopicClassifier()
        self.logger = logging.getLogger(__name__)

    def batch_vectorize(self, records: List[Dict[str, Any]], batch_size: int = 100) -> List[Dict[str, Any]]:
        """批量處理記錄"""
        result_records = []
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            
            try:
                processed_batch = []
                
                for record in batch:
                    # 處理每筆記錄
                    processed_record = self.process_record(record)
                    processed_batch.append(processed_record)
                
                result_records.extend(processed_batch)
                print(f"已向量化記錄 {i+1} 到 {i+len(batch)} (共 {len(records)} 筆)")
                
            except Exception as e:
                self.logger.error(f"處理批次 {i} 到 {i+batch_size} 時發生錯誤: {str(e)}")
                # 繼續處理下一批
        
        return result_records
    
    def process_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """處理單筆記錄"""
        try:
            result = record.copy()
            
            # 從 keyword 確定主要對象
            primary_target = record.get('keyword', '').strip().lower()
            
            # 處理三個關鍵欄位
            cleaned_content = self.text_processor.process_text(record.get('content_text', ''))
            cleaned_title = self.text_processor.process_text(record.get('article_title', ''))
            
            # 分析文本中提到的咖啡店
            content_mentions = self.text_processor.detect_coffee_shops(record.get('content_text', ''))
            title_mentions = self.text_processor.detect_coffee_shops(record.get('article_title', ''))
            
            # 確定評論的真正目標
            mentioned_targets = content_mentions.union(title_mentions)
            
            # 如果文本中明確提到了其他咖啡店但不是主要目標，記錄為比較
            is_comparison = False
            compared_shops = []
            
            if primary_target == 'cama' and '路易莎' in mentioned_targets:
                is_comparison = True
                compared_shops.append('路易莎')
            elif primary_target == '路易莎' and 'cama' in mentioned_targets:
                is_comparison = True
                compared_shops.append('cama')
                
            result['is_comparison'] = is_comparison
            result['compared_shops'] = compared_shops
            
            # 分析情感
            content_sentiment, content_magnitude = self.sentiment_analyzer.analyze_text_sentiment(cleaned_content)
            title_sentiment, title_magnitude = self.sentiment_analyzer.analyze_text_sentiment(cleaned_title)
            
            result['content_sentiment'] = content_sentiment
            result['content_magnitude'] = content_magnitude
            result['title_sentiment'] = title_sentiment
            result['title_magnitude'] = title_magnitude
            result['keyword_sentiment'] = 0  # 關鍵字本身通常沒有情感
            
            # 計算主題分類的文字
            combined_text = f"{cleaned_title} {cleaned_content}"
            result['processed_text'] = combined_text
            
            return result
                
        except Exception as e:
            self.logger.error(f"處理記錄 {record.get('id', 'unknown')} 時發生錯誤: {str(e)}")
            return record
            
    def calculate_results(self, records: List[Dict[str, Any]]) -> List[Tuple[int, str, int, str]]:
        """計算最終結果"""
        results = []
        
        for record in records:
            try:
                # 計算情感
                sentiment, score = self.sentiment_analyzer.calculate_sentiment(record)
                
                # 分類主題
                topic = self.topic_classifier.classify(record['processed_text'])
                
                # 添加到結果
                results.append((record['id'], sentiment, score, topic))
                
            except Exception as e:
                self.logger.error(f"計算記錄 {record.get('id', 'unknown')} 的結果時發生錯誤: {str(e)}")
                
        return results