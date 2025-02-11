# config.py

"""
PTT 爬蟲配置文件
包含所有要爬取的看板分類
"""

# 基本討論看板
GENERAL_BOARDS = [
    "Gossiping",  # 八卦板
    "WomenTalK",  # 女性板
    "Stock",  # 股票板
    "ask",  # 問答板
]

# 美食與飲品相關看板
FOOD_BEVERAGE_BOARDS = [
    "Food",  # 美食板
    "Drink",  # 飲料板
    "Tea",  # 茶板
    "Coffee",  # 咖啡板
    "HerbTea",  # 花草茶板
    "Starbucks",  # 星巴克板
    "Barista",  # 咖啡師板
    "CAFENCAKE",  # 咖啡廳板
    "fastfood",  # 速食板
    "Snacks",  # 零食板
]

# 消費與購物相關看板
CONSUMER_BOARDS = [
    "CVS",  # 便利商店板
    "Lifeismoney",  # 省錢板
    "toberich",  # 理財板
    "MobilePay",  # 行動支付板
    "creditcard",  # 信用卡板
    "hypermall",  # 量販店板
    "e-shopping",  # 網購板
    "consumer",  # 消費板
]

# 工作與職涯相關看板
CAREER_BOARDS = [
    "job",  # 工作板
    "part-time",  # 打工板
    "Actuary",  # 精算板
    "Atom_Boyz",  # 原子小金剛板
]

# 新北市看板
NEW_TAIPEI_BOARDS = [
    "BigBanciao",  # 板橋板
    "BigSanchung",  # 三重板
    "HsinChuang",  # 新莊板
    "HsinTien",  # 新店板
    "LinKou",  # 林口板
    "San-Ying",  # 三鶯板
    "Shu-Lin",  # 樹林板
    "ShuangHe",  # 雙和板
    "Sijhih",  # 汐止板
    "TaiShan",  # 泰山板
    "TamShui",  # 淡水板
    "TuCheng",  # 土城板
    "WuGu-BaLi",  # 五股八里板
]

# 台北市看板
TAIPEI_BOARDS = [
    "BigPeitou",  # 北投板
    "BigShiLin",  # 士林板
    "Daan",  # 大安板
    "Datong",  # 大同板
    "HsinYi",  # 信義板
    "Nangang",  # 南港板
    "Neihu",  # 內湖板
    "SongShan",  # 松山板
    "Taipei",  # 台北板
    "Wanhua",  # 萬華板
    "Wen-Shan",  # 文山板
    "Zhongshan",  # 中山板
    "Zhongzheng",  # 中正板
]

# 基隆與周邊看板
KEELUNG_BOARDS = [
    "Keelung",  # 基隆板
    "N_E_Coastal",  # 東北角板
    "North_Coast",  # 北海岸板
]

# 桃竹地區看板
TAOYUAN_HSINCHU_BOARDS = [
    "ChungLi",  # 中壢板
    "Hsinchu",  # 新竹板
    "Taoyuan",  # 桃園板
]

# 整合北部地區看板
NORTHERN_BOARDS = (
    NEW_TAIPEI_BOARDS + TAIPEI_BOARDS + KEELUNG_BOARDS + TAOYUAN_HSINCHU_BOARDS
)

# 中部地區看板
CENTRAL_BOARDS = [
    "ChangHua",  # 彰化板
    "FengYuan",  # 豐原板
    "Miaoli",  # 苗栗板
    "Nantou",  # 南投板
    "TaichungBun",  # 台中報報板
    "TaichungCont",  # 台中建言板
    "Yunlin",  # 雲林板
]

# 南部地區看板
SOUTHERN_BOARDS = [
    "Chiayi",  # 嘉義板
    "Daliao",  # 大寮板
    "FongShan",  # 鳳山板
    "Kaohsiung",  # 高雄板
    "Linyuan",  # 林園板
    "PingTung",  # 屏東板
    "Tainan",  # 台南板
]

# 東部與外島地區看板
EASTERN_OFFSHORE_BOARDS = [
    "Hualien",  # 花蓮板
    "I-Lan",  # 宜蘭板
    "Taitung",  # 台東板
    "Jinmen",  # 金門板
    "Matsu",  # 馬祖板
]

# 旅遊相關看板
TRAVEL_BOARDS = [
    "PH-sea",  # 菲律賓海板
    "Tai-travel",  # 台灣旅遊板
    "Taiwan319",  # 台灣319鄉鎮板
]

# 整合所有看板
ALL_BOARDS = (
    GENERAL_BOARDS
    + FOOD_BEVERAGE_BOARDS
    + CONSUMER_BOARDS
    + CAREER_BOARDS
    + NEW_TAIPEI_BOARDS
    + TAIPEI_BOARDS
    + KEELUNG_BOARDS
    + TAOYUAN_HSINCHU_BOARDS
    + CENTRAL_BOARDS
    + SOUTHERN_BOARDS
    + EASTERN_OFFSHORE_BOARDS
    + TRAVEL_BOARDS
)

# 維護說明
# 1. 要新增看板時，根據類別加入相應的列表中
# 2. 確保看板名稱正確，且符合 PTT 規範
# 3. ALL_BOARDS 會自動包含所有分類中的看板