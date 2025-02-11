from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

class GoogleMapsScraper:
    def __init__(self):
        self.options = self._setup_chrome_options()
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.processed_reviews = set()
        self.valid_reviews = []
        
    def _setup_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    def click_review_tab(self):
        try:
            # 等待並點擊評論標籤
            review_tab = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[role="tab"][data-tab-index="1"]')
            ))
            review_tab.click()
            time.sleep(2)
            
            # 使用 XPath 定位排序按鈕
            sort_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-label='排序評論']")
            ))
            self.driver.execute_script("arguments[0].click();", sort_button)
            time.sleep(1)
            
            # 選擇最新評論
            newest_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='menuitemradio'][contains(., '最新')]")
            ))
            newest_option.click()
            time.sleep(2)
            
        except Exception as e:
            print(f"點擊排序按鈕時發生錯誤: {e}")
            self.driver.save_screenshot("error_screenshot.png")

    def scroll_reviews(self, max_scrolls=10):
        try:
            # 等待評論容器載入
            time.sleep(2)
            
            # 找到正確的評論容器：div.m6QErb DxyBCb kA9KIf dS8AEf
            scrollable_div = self.driver.find_element(
                By.CSS_SELECTOR, 
                'div.m6QErb.DxyBCb.kA9KIf.dS8AEf'
            )
            
            previous_count = 0
            for i in range(max_scrolls):
                # 執行滾動
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight', 
                    scrollable_div
                )
                
                # 添加隨機等待時間
                time.sleep(random.uniform(1.5, 2.5))
                
                # 計算當前評論數
                current_reviews = self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')
                current_count = len(current_reviews)
                
                print(f"已滾動 {i+1} 次，當前評論數: {current_count}")
                
                # 檢查是否已到底部
                if current_count == previous_count:
                    print(f"滾動完成，共載入 {current_count} 則評論")
                    break
                    
                previous_count = current_count
                
        except Exception as e:
            print(f"滾動評論時發生錯誤: {e}")
            self.driver.save_screenshot("scroll_error.png")

    def extract_reviews(self, store_name):
        reviews = self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf')
        print(f"找到 {len(reviews)} 則評論")
        
        for review in reviews:
            try:
                review_id = review.get_attribute('data-review-id')
                
                if review_id not in self.processed_reviews:
                    # 檢查評論內容
                    content = review.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                    if not content.strip():
                        continue
                    
                    # 提取評分
                    stars = review.find_elements(By.CSS_SELECTOR, 'span.hCCjke')
                    rating = sum(1 for star in stars if 'elGi1d' in star.get_attribute('class'))
                    
                    print(f"評分: {rating}, 內容: {content[:50]}...")
                    
                    self.valid_reviews.append({
                        'store_name': store_name,
                        'rating': rating,
                        'content': content
                    })
                    
                    self.processed_reviews.add(review_id)
                    
            except Exception as e:
                print(f"提取評論時發生錯誤: {e}")
                continue

    def scrape_single_location(self, url, store_name):
        try:
            print(f"開始處理: {url}")
            self.driver.get(url)
            time.sleep(3)  # 等待頁面載入
            
            # 點擊評論頁籤和排序
            self.click_review_tab()
            
            # 滾動載入評論
            self.scroll_reviews()
            
            # 提取評論
            self.extract_reviews(store_name)
            
            return self.valid_reviews
            
        except Exception as e:
            print(f"發生錯誤: {e}")
            return []
        
        finally:
            self.driver.quit()

    def save_to_csv(self, filename):
        if not self.valid_reviews:
            print("沒有評論資料可供儲存")
            return
            
        df = pd.DataFrame(self.valid_reviews)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"成功儲存 {len(df)} 則評論到 {filename}")

def main():
    # 測試用的單一 URL
    test_url = "https://www.google.com/maps/place/cama+caf%C3%A9+%E5%8F%B0%E6%9D%B1%E9%90%B5%E8%8A%B1%E6%9D%91%E5%BA%97/@22.7508257,121.1464582,17z/data=!3m1!4b1!4m6!3m5!1s0x346fb92c1196c405:0x449c490d6af4d828!8m2!3d22.7508257!4d121.1490331!16s%2Fg%2F11vbjtbttn?authuser=1&entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D"  # 替換成你要測試的 Google Maps URL
    test_store = "測試店家"
    
    scraper = GoogleMapsScraper()
    reviews = scraper.scrape_single_location(test_url, test_store)
    scraper.save_to_csv('test_reviews.csv')

if __name__ == "__main__":
    main()