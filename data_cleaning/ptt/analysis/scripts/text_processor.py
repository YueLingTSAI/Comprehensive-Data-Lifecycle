import re
import logging
from typing import Dict, Set, List, Tuple, Any

class TextProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.coffee_shops = {
            "cama": {
                "name": "CAMA",
                "variants": [
                    "CAMA", "Cama", "cama", "cama café", "cama咖啡", "卡瑪"
                ],
            },
            "louisa": {
                "name": "路易莎",
                "variants": [
                    "路易莎", "Louisa", "louisa", "Louisa Coffee", "路易莎咖啡"
                ],
            },
        }
        
        # 初始化關鍵詞組
        self.key_patterns = self._init_key_patterns()
        
    def _init_key_patterns(self):
        """初始化關鍵詞組"""
        coffee_shop_variants = []
        for shop in self.coffee_shops.values():
            coffee_shop_variants.extend(shop['variants'])
            
        return [
            # 評價相關 - 包含PTT常見用語和表達方式
            (rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(好|爛|差|棒|讚|推薦|失望|不錯|可以|不行|神|雷|佳|糟|屌打|吊打|完勝|秒殺|屌|強|弱|猛|遜|有質感|無敵|超越|值得|不值|去過|必去|別去|可惜|驚艷|驚喜|驚嚇|喜歡|不喜歡|愛|恨|慘|慘不忍睹|爆炸|炸裂|頂|頂級|頂尖|一流|二流|三流|高級|坑|雞肋|垃圾|神作|傑作|經典|後悔|不後悔|上當|虧|賺到|失望|再訪|不再訪|超神|超鬧)", '評價'),
            
            # 價格相關 - 包含台灣特有金錢表達
            (rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(價格|費用|花費|貴|便宜|划算|性價比|CP值|物超所值|不划算|不合理|太貴|超貴|小資|奢侈|經濟|實惠|親民|大眾|高端|價位|收費|成本|定價|標價|價錢|特價|優惠|折扣|打折|促銷|高價|低價|中價|$$|＄|元|塊|錢|台幣|新台幣)", '價格'),
            
            # 服務相關 - 包含台灣特有服務態度表達
            (rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(服務|店員|態度|熱情|親切|冷淡|服務生|店長|老闆|客服|櫃檯|收銀|接待|服務員|服務態度|招待|招呼|笑容|笑臉|臉色|黑臉|白眼|翻白眼|不耐煩|不理人|理睬|友善|不友善|禮貌|有禮|沒禮貌|粗魯|兇|凶)", '服務'),
            
            # 品質相關 - 包含台灣特有咖啡文化和表達
            (rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(咖啡|飲料|餐點|口感|品質|味道|品項|風味|香氣|香味|濃郁|淡|苦|酸|甜|澀|香|辛辣|鹹|澀|甘|回甘|醇|醇厚|醇香|醇美|厚實|薄弱|層次|層次感|複雜度|口味|風格|特色|特點|調性|獨特|獨家|特調|配方)", '品質'),
            
            # 環境相關 - 包含台灣特有空間和環境表達
            (rf"({'|'.join(coffee_shop_variants)}).{{0,50}}(環境|空間|氣氛|座位|裝修|裝潢|佈置|設計|風格|布置|採光|光線|燈光|照明|明亮|昏暗|窗戶|採光|通風|空調|冷氣|暖氣|溫度|濕度|熱|冷|涼爽|悶熱|舒適|不舒|comfortable|舒服|舒坦|自在|愜意)", '環境')
        ]
        
    def clean_text(self, text: str) -> str:
        """清理文本"""
        if not text or not isinstance(text, str):
            return ""
            
        # 移除特殊符號和額外空白
        text = re.sub(r'--+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        # 移除雜訊詞
        noise_words = ['發文者:', '看板:', 'Re:', 'Fw:']
        for word in noise_words:
            text = text.replace(word, '')
        
        return text.strip()
        
    def extract_key_info(self, text: str) -> str:
        """提取關鍵信息"""
        if not text or not isinstance(text, str):
            return ""
            
        extracted = []
        for pattern, category in self.key_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                extracted.append(match.group(0))
        
        return ' '.join(extracted)
        
    def process_text(self, text: str) -> str:
        """處理文本"""
        if not text or not isinstance(text, str):
            return ""
            
        # 基本清理
        cleaned_text = self.clean_text(text)
        
        # 提取關鍵資訊
        key_info = self.extract_key_info(cleaned_text)
        
        # 處理比較語句
        comparisons = self.extract_comparisons(cleaned_text)
        
        # 合併結果
        combined = []
        if key_info:
            combined.append(key_info)
        if comparisons:
            combined.append(comparisons)
            
        return ' '.join(combined) if combined else cleaned_text
        
    def extract_comparisons(self, text: str) -> str:
        """提取比較語句"""
        extracted = []
        
        # 比較關鍵詞
        comparison_keywords = ['比', '勝過', '超過', '強過', '屌打', '吊打', '完勝', '不如', '輸給']
        coffee_brands = ['路易莎', '星巴克', 'cama', 'CAMA', '伯朗', '丹堤']
        
        for keyword in comparison_keywords:
            if keyword in text.lower():
                for brand in coffee_brands:
                    pattern1 = rf"{keyword}.{{0,20}}{brand}"
                    pattern2 = rf"{brand}.{{0,20}}{keyword}"
                    
                    for pattern in [pattern1, pattern2]:
                        matches = re.finditer(pattern, text, re.IGNORECASE)
                        for match in matches:
                            extracted.append(match.group(0))
                            
        return ' '.join(extracted)
        
    def detect_coffee_shops(self, text: str) -> Set[str]:
        """檢測文本中提到的咖啡店"""
        mentioned_shops = set()
        
        # 檢測 CAMA
        for variant in self.coffee_shops['cama']['variants']:
            if variant.lower() in text.lower():
                mentioned_shops.add('cama')
                break
                
        # 檢測路易莎
        for variant in self.coffee_shops['louisa']['variants']:
            if variant.lower() in text.lower():
                mentioned_shops.add('路易莎')
                break
                
        return mentioned_shops