import requests
import pandas as pd
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from db_config import save_to_db, init_db
from sqlalchemy import and_

# 初始化資料庫連接和表格
engine, Base, Session, session, Dcard = init_db()
load_dotenv()


def should_skip_title(title):
    """檢查標題是否應該被跳過"""
    skip_patterns = [
        "的文章搜尋結果",
        "的搜尋結果",
    ]
    return any(pattern in title for pattern in skip_patterns)


def check_review_exists(cafe, title, search_date, session):
    """檢查評論是否已存在於資料庫中"""
    existing_review = (
        session.query(Dcard)
        .filter(
            and_(
                Dcard.cafe == cafe,
                Dcard.title == title,
                Dcard.search_date == search_date,
            )
        )
        .first()
    )
    return existing_review is not None


def search_cafe_reviews(api_key, cx, cafe_keywords, max_requests_per_cafe=25):
    base_url = "https://www.googleapis.com/customsearch/v1"
    all_results = []
    requests_count = 0

    search_query = " OR ".join(
        [f'"{keyword}"' for keyword in cafe_keywords["variants"]]
    )

    # 設定日期範圍 (近5年)
    date_restrict = "d1825"  # 限制在最近5年內的結果 (365 * 5 = 1825天)

    start_index = 1
    while requests_count < max_requests_per_cafe:
        params = {
            "key": api_key,
            "cx": cx,
            "q": f"site:dcard.tw ({search_query}) (評價 OR 心得) after:2019-01-01",  # 限制 2019 年後的結果
            "num": 10,
            "start": start_index,
            "sort": "date",  # 依日期排序
            "dateRestrict": date_restrict,
        }

        try:
            requests_count += 1
            print(f"正在進行第 {requests_count} 次請求 ({cafe_keywords['name']})")
            print(f"搜尋 2021 年後的評價...")

            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code != 200:
                print(f"API 錯誤: {response.status_code}")
                print(f"錯誤訊息: {data.get('error', {}).get('message', '未知錯誤')}")
                break

            if "items" not in data:
                print(f"沒有更多結果")
                break

            found_any = False
            for item in data["items"]:
                title = item.get("title", "")

                # 檢查標題是否應該被跳過
                if should_skip_title(title):
                    print(f"跳過搜尋結果頁面: {title[:50]}...")
                    continue

                text_to_check = (title + " " + item.get("snippet", "")).lower()

                if any(
                    keyword.lower() in text_to_check
                    for keyword in cafe_keywords["variants"]
                ):
                    current_time = datetime.now()

                    # 檢查是否已存在相同評論
                    if not check_review_exists(
                        cafe_keywords["name"],
                        title,
                        current_time,
                        session,
                    ):
                        result = {
                            "cafe": cafe_keywords["name"],
                            "title": title,
                            "link": item.get("link", ""),
                            "content": item.get("snippet", ""),
                            "source": "Dcard",
                            "search_date": current_time,
                        }
                        all_results.append(result)
                        found_any = True
                        print(f"找到新評價: {result['title'][:50]}...")
                    else:
                        print(f"跳過重複評價: {title[:50]}...")

            if not found_any:
                print("本頁未找到相關新評價")

            start_index += len(data["items"])
            if len(data["items"]) < 10:
                print("到達最後一頁")
                break

            time.sleep(3)  # 避免請求過於頻繁

        except Exception as e:
            print(f"搜尋時發生錯誤: {str(e)}")
            break

    return all_results, requests_count


def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    if not api_key or not cx:
        print("錯誤：未設定環境變數 GOOGLE_API_KEY 或 GOOGLE_SEARCH_ENGINE_ID")
        return

    cafe_keywords = {
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

    max_requests_per_cafe = 25
    all_reviews = []
    total_requests = 0

    for cafe in cafe_keywords.values():
        print(f"\n開始搜尋 {cafe['name']} 的評價...")
        reviews, requests_used = search_cafe_reviews(
            api_key, cx, cafe, max_requests_per_cafe
        )
        total_requests += requests_used
        all_reviews.extend(reviews)
        print(f"完成 {cafe['name']} 搜尋，使用了 {requests_used} 次請求")

    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df = df.drop_duplicates(subset=["link"])

        # 儲存到資料庫並獲取統計資訊
        success_count, duplicate_count = save_to_db(df.to_dict("records"))

        print(f"\n=== 搜尋完成 ===")
        print(f"總共使用 {total_requests} 次 API 請求")
        print(f"搜尋到的不重複評價: {len(df)} 筆")
        print(f"成功新增到資料庫: {success_count} 筆")
        print(f"資料庫中已存在: {duplicate_count} 筆")
    else:
        print("沒有找到任何評價")


if __name__ == "__main__":
    main()
