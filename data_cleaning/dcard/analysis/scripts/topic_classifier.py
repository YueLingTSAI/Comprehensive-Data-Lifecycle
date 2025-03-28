class TopicClassifier:
    def __init__(self):
        self.topics = {
            '咖啡品質': [
                '品質', '口感', '味道', '風味', '豆子', '咖啡', '回甘', '順口', '濃郁', '淡', '苦', '香醇', '濃縮',
                '生豆', '烘焙', '手沖', '義式', '美式', '拿鐵', '焦苦', '酸味', '果香', '花香', '醇厚', '年份',
                '產地', '水準', '萃取'
            ],
            '服務體驗': [
                '服務', '態度', '店員', '人員', '店長', '熱情', '貼心', '友善', '慢', '不理人', '專業', '耐心', '熱忱',
                '招呼', '建議', '推薦', '解說', '說明', '介紹', '親切', '禮貌', '笑容', '溝通', '應對', '協助'
            ],
            '價格優惠': [
                '價格', '貴', '便宜', '划算', '值得', '便利', 'CP值', '優惠', '折扣', '活動', '性價比',
                '定價', '特價', '降價', '漲價', '超值', '花費', '成本', '預算', '促銷', '限時'
            ],
            '環境氛圍': [
                '環境', '空間', '座位', '店面', '裝潢', '衛生', '吵雜', '安靜', '燈光', '氣氛', '音樂', '舒適',
                '乾淨', '整潔', '採光', '通風', '溫度', '冷氣', '擺設', '裝置', '風格', '設計感', '氛圍',
                'wifi', '插座', '停車'
            ],
            '服務效率': [
                '等太久', '超快', '出餐慢', '排隊', '等候', '快速', '拖延',
                '效率', '準時', '即時', '流程', '調度', '忙碌', '人手', '尖峰', '離峰'
            ],
            '包裝設計': [
                '紙杯', '吸管', '環保', '包裝', '外帶', '設計',
                '杯套', '提袋', '封口', '材質', '容器', '重複使用', '環保袋', '保溫'
            ],
            '餐點選擇': [
                '可頌', '蛋糕', '司康', '餐點', '甜點', '點心', '麵包', '輕食', '小食',
                '三明治', '鹹食', '沙拉', '套餐', '早餐', '下午茶', '菜單', '品項', '選擇'
            ],
            '行銷活動': [
                '優惠券', '折價券', '集點', '買一送一', '特價', '促銷', '限時', '會員', 'APP', '點數', 'CAMA pay',
                '信用卡', '行動支付', '電子支付', '活動時間', '限定', '快閃', '合作', '方案', '好康',
                '行銷', '宣傳', '廣告', '社群', 'IG', 'FB', '臉書', '網路', '曝光', '網紅', '直播'
            ],
            '工作環境': [
                '打工', '兼職', '工讀', '面試', '薪資', '時薪', '排班', '職缺', '應徵', '工作', '上班', '員工',
                '福利', '獎金', '加班', '升遷', '工時', '休假', '請假', '在職', '離職',
                '勞健保', '教育訓練', '考核', '升遷', '管理', '團隊', '主管', '正職', '績效'
            ],
            '品牌形象': [
                '品牌', '形象', '知名度', '口碑', '名氣', '評價', '聲譽', '風評',
                '連鎖', '規模', '企業', '文化', '理念', '經營', '特色', '風格',
                '在地', '國際', '發展', '歷史', '傳統', '創新'
            ],
            '客戶體驗': [
                '體驗', '感受', '印象', '回憶', '推薦', '建議', '回饋',
                '習慣', '偏好', '需求', '期待', '滿意', '失望', '抱怨',
                '顧客', '消費者', '客人', '回訪', '忠誠'
            ]
        }

    def classify(self, text: str) -> str:
        text = text.lower()
        found_topics = []
        for topic, keywords in self.topics.items():
            if any(keyword in text for keyword in keywords):
                found_topics.append(topic)
        
        return '、'.join(found_topics) if found_topics else '其他'
