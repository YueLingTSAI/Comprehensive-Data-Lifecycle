import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import random
from typing import Optional, Dict, List
from urllib.parse import quote

import ptt_db as db
from ptt_config import ALL_BOARDS


class PTTCrawler:
    def __init__(self):
        self.base_url = "https://www.ptt.cc"
        self.headers = {"User-Agent": "Mozilla/5.0", "Cookie": "over18=1"}
        self.boards = ALL_BOARDS

        # 定義咖啡店關鍵字
        self.cafe_keywords = {
            "cama": [
                "cama",
                "CAMA",
                "Cama",
                "CAMA咖啡",
                "CAMA café",
                "CAMA coffee",
            ],
            "路易莎": [
                "路易莎",
                "louisa",
                "LOUISA",
                "Louisa",
                "LOUISA COFFEE",
                "Louisa Coffee",
                "路易莎咖啡",
                "路易莎門市",
            ],
        }

        # 計數器
        self.total_pages = 0
        self.total_articles = 0
        self.total_comments = 0
        self.start_time = None
        self.time_limit = 300  # 設定10分鐘限制

    def check_cafe_keywords(self, text: str) -> Optional[str]:
        """檢查文字是否包含咖啡店關鍵字，返回對應的咖啡店名稱"""
        if not text:
            return None

        text_lower = text.lower()
        for cafe, keywords in self.cafe_keywords.items():
            if any(keyword.lower() in text_lower for keyword in keywords):
                return cafe
        return None

    def print_progress(self):
        """顯示爬蟲進度"""
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        print("\n" + "=" * 50)
        print(f"爬蟲進度報告：")
        print(f"已處理頁面數：{self.total_pages}")
        print(f"已儲存文章數：{self.total_articles}")
        print(f"已儲存推文數：{self.total_comments}")
        print(f"已執行時間：{elapsed_time:.1f} 秒")
        print("=" * 50)

    def is_time_expired(self) -> bool:
        """檢查是否超過時間限制"""
        if not self.start_time:
            return False
        return (datetime.now() - self.start_time).total_seconds() >= self.time_limit

    def get_article_content(self, url: str) -> Optional[Dict]:
        """獲取文章內容和推文"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # 取得主要內容
            main_content = soup.find(id="main-content")
            if not main_content:
                return None

            # 取得發文時間
            meta_values = soup.find_all("span", class_="article-meta-value")
            post_time = datetime.now()  # 預設值
            if meta_values and len(meta_values) >= 4:
                try:
                    time_str = meta_values[3].text.strip()
                    post_time = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
                except ValueError:
                    pass

            # 處理文章內容
            content_copy = BeautifulSoup(str(main_content), "html.parser")
            for meta in content_copy.find_all(
                ["div", "span"],
                class_=["article-metaline", "article-metaline-right", "f2"],
            ):
                meta.decompose()

            # 取得推文
            pushes = main_content.find_all("div", class_="push")
            comments = []
            for push in pushes:
                try:
                    author = push.find("span", class_="f3 hl push-userid").text.strip()
                    content = push.find("span", class_="f3 push-content").text.strip()
                    content = content.lstrip(":").strip()
                    comments.append({"author": author, "content": content})
                except AttributeError:
                    continue

            # 清理主文內容
            for push in content_copy.find_all("div", class_="push"):
                push.decompose()
            content = content_copy.get_text().strip()

            return {"content": content, "post_time": post_time, "comments": comments}

        except Exception as e:
            print(f"處理文章時發生錯誤 ({url}): {e}")
            return None

    def search_board_with_keyword(self, board: str, keyword: str, page: int) -> bool:
        """使用關鍵字搜尋特定看板"""
        search_url = (
            f"{self.base_url}/bbs/{board}/search?page={page}&q={quote(keyword)}"
        )
        print(f"\n搜尋 {board} 板第 {page} 頁，關鍵字: {keyword}")

        try:
            if db.is_url_crawled(search_url):
                print(f"跳過已爬取的頁面: {search_url}")
                return False

            response = requests.get(search_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # 標記頁面已爬取
            db.store_crawled_page(search_url)
            self.total_pages += 1

            # 尋找搜尋結果
            articles = soup.find_all("div", class_="r-ent")
            if not articles:
                print(f"在 {board} 板找不到更多 {keyword} 的搜尋結果")
                return False

            for article in articles:
                if self.is_time_expired():
                    return False

                title_div = article.find("div", class_="title")
                if not title_div or not title_div.find("a"):
                    continue

                title = title_div.find("a").text.strip()
                link = self.base_url + title_div.find("a")["href"]

                # 獲取文章內容
                article_data = self.get_article_content(link)
                if not article_data:
                    continue

                # 檢查文章內容是否包含關鍵字
                cafe = self.check_cafe_keywords(article_data["content"])
                if cafe:
                    # 儲存文章
                    db.store_mention(
                        keyword=cafe,
                        article_title=title,
                        content_text=article_data["content"],
                        content_type="article",
                        post_time=article_data["post_time"],
                        article_url=link,
                    )
                    self.total_articles += 1
                    print(f"找到相關文章: {title[:50]}... ({cafe})")

                # 處理推文
                for comment in article_data["comments"]:
                    comment_cafe = self.check_cafe_keywords(comment["content"])
                    if comment_cafe:
                        db.store_mention(
                            keyword=comment_cafe,
                            article_title=title,
                            content_text=comment["content"],
                            content_type="comment",
                            post_time=article_data["post_time"],
                            article_url=link,
                            comment_author=comment["author"],
                        )
                        self.total_comments += 1
                        print(
                            f"找到相關推文：{comment['content'][:30]}... ({comment_cafe})"
                        )

                time.sleep(random.uniform(2, 4))  # 短暫休息避免過度請求

            return True

        except Exception as e:
            print(f"搜尋看板時發生錯誤: {e}")
            return False

    def run(self):
        """執行爬蟲"""
        self.start_time = datetime.now()
        print(f"開始搜尋 PTT 文章...")
        print(f"時間限制: {self.time_limit} 秒")

        # 對每個看板進行搜尋
        for board in self.boards:
            print(f"\n開始搜尋看板: {board}")

            # 搜尋每個咖啡店的關鍵字
            for cafe, keywords in self.cafe_keywords.items():
                # 使用每個關鍵字進行搜尋
                for keyword in keywords:
                    page = 1
                    while (
                        not self.is_time_expired() and page <= 30
                    ):  # 限制每個關鍵字最多搜尋30頁
                        if not self.search_board_with_keyword(board, keyword, page):
                            break
                        page += 1
                        self.print_progress()

                        # 隨機休息 2-4 秒
                        sleep_time = random.uniform(2, 4)
                        print(f"\n休息 {sleep_time:.1f} 秒...")
                        time.sleep(sleep_time)

        print("\n爬蟲完成！")
        self.print_progress()


def main():
    # 確保資料表存在
    db.create_tables()

    # 開始爬取
    crawler = PTTCrawler()
    crawler.run()


if __name__ == "__main__":
    main()
