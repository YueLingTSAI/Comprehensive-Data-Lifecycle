from google.cloud import language_v1
import logging
import re
from .topic_classifier import TopicClassifier


class ContentAnalyzer:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()
        self.logger = logging.getLogger(__name__)
        self.topic_classifier = TopicClassifier()

        # 定義咖啡店名稱變體
        self.coffee_shops = {
            "cama": {
                "name": "CAMA",
                "variants": [
                    "CAMA",
                    "Cama",
                    "cama",
                    "cama café",
                    "cama咖啡",
                ],
            },
            "louisa": {
                "name": "路易莎",
                "variants": [
                    "路易莎",
                    "Louisa",
                    "louisa",
                    "Louisa Coffee",
                    "路易莎咖啡",
                ],
            },
        }

    def clean_text(self, text: str) -> str:
        # 移除日期時間格式
        text = re.sub(r"\d{1,2}\s+days?\s+ago", "", text)
        text = re.sub(r"\d{1,2}\s+hours?\s+ago", "", text)
        text = re.sub(r"[A-Za-z]+\s+\d{1,2},\s+\d{4}", "", text)

        # 移除互動資訊
        text = re.sub(r"心情\d+・留言\d+", "", text)
        text = re.sub(r"愛心\s*\d+", "", text)
        text = re.sub(r"收藏\s*\d*", "", text)

        # 移除特殊符號和額外空白
        text = re.sub(r"[・·]", " ", text)
        text = re.sub(r"\s+", " ", text)

        # 移除雜訊詞
        noise_words = ["thumbnail", "sticker", "#心得", "#請益", "匿名", "B1", "回覆"]
        for word in noise_words:
            text = text.replace(word, "")

        return text.strip()

    def extract_key_info(self, text: str) -> str:
        # 獲取所有咖啡店變體
        coffee_shop_variants = []
        for shop in self.coffee_shops.values():
            coffee_shop_variants.extend(shop["variants"])

        # 定義關鍵詞組
        key_patterns = [
            (
                rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(好|爛|差|棒|讚|推薦|失望|不錯|可以|不行)",
                "評價",
            ),
            (
                rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(價格|費用|花費|貴|便宜|划算).{{0,30}}",
                "價格",
            ),
            (
                rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(服務|店員|態度|熱情|親切|冷淡).{{0,30}}",
                "服務",
            ),
            (
                rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(咖啡|飲料|餐點|口感|品質|味道).{{0,30}}",
                "品質",
            ),
            (
                rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(環境|空間|氣氛|座位).{{0,30}}",
                "環境",
            ),
        ]

        extracted = []
        for pattern, category in key_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                extracted.append(match.group(0))

        return " ".join(extracted)

    def process_text(self, text: str) -> str:
        # 基本清理
        cleaned_text = self.clean_text(text)

        # 提取關鍵資訊
        key_info = self.extract_key_info(cleaned_text)

        return key_info if key_info else cleaned_text

    def analyze_sentiment(self, cafe: str, title: str, content: str) -> tuple:
        try:
            # 分別處理三個部分的文本
            cleaned_content = self.process_text(content)
            cleaned_title = self.process_text(title)
            cleaned_cafe = self.process_text(cafe)

            # 分別進行情感分析
            content_sentiment = self.get_sentiment_score(cleaned_content)
            title_sentiment = self.get_sentiment_score(cleaned_title)
            cafe_sentiment = self.get_sentiment_score(cleaned_cafe)

            # 加權計算總分 (content 50%, title 40%, cafe 10%)
            weighted_score = (
                content_sentiment * 0.5 + title_sentiment * 0.4 + cafe_sentiment * 0.1
            )

            # 轉換到 1-5 分數範圍
            normalized_score = round((weighted_score + 1) * 2.5)
            final_score = int(max(1, min(5, normalized_score)))

            sentiment_levels = {
                5: "強烈正面",
                4: "正面",
                3: "中性",
                2: "負面",
                1: "強烈負面",
            }

            return sentiment_levels[final_score], final_score

        except Exception as e:
            self.logger.error(f"Sentiment analysis error: {str(e)}")
            return "中性", 3

    def get_sentiment_score(self, text: str) -> float:
        try:
            if not text.strip():
                return 0

            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language="zh-TW",
            )

            sentiment = self.client.analyze_sentiment(
                request={"document": document}
            ).document_sentiment

            # 根據情感強度調整分數
            score = sentiment.score
            if sentiment.magnitude > 1.0:
                if score > 0:
                    score = min(1, score + 0.2)
                elif score < 0:
                    score = max(-1, score - 0.2)

            return score

        except Exception as e:
            self.logger.error(f"Error getting sentiment score: {str(e)}")
            return 0

    def classify_topic(self, text: str) -> str:
        return self.topic_classifier.classify(text)
