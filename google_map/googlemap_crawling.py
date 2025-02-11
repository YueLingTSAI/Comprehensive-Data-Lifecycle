from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import os

class GoogleMapsBatchScraper:
    def __init__(self, headless=True):
        # 設定 Chrome 選項
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        
        # 添加額外的 Chrome 選項來處理各種問題
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-software-rasterizer")
        self.options.add_argument('--ignore-gpu-blocklist')
        self.options.add_argument('--enable-unsafe-swiftshader')
        self.options.add_argument("--disable-web-security")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument('--force-device-scale-factor=1')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        # 初始化 WebDriver
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        
        # 設定更長的等待時間
        self.wait = WebDriverWait(self.driver, 20)  # 增加等待時間至 20 秒
        
        # 設定視窗大小
        self.driver.set_window_size(1920, 1080)
        
    def load_urls_from_csv(self, csv_files):
        """從多個 CSV 文件載入 URL"""
        urls = []
        for file in csv_files:
            df = pd.read_csv(file, usecols=["urls"])
            urls.extend(df['urls'].tolist())
        return urls

    def open_page(self, url):
        """打開並初始化頁面"""
        try:
            self.driver.get(url)
            
            # 等待頁面基本元素載入
            time.sleep(5)  # 增加初始等待時間
            
            # 等待並點擊評論按鈕
            review_tab = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[role="tab"][data-tab-index="1"]'))
            )
            
            # 確保按鈕在可視範圍內
            self.driver.execute_script("arguments[0].scrollIntoView(true);", review_tab)
            time.sleep(2)
            
            # 使用 JavaScript 點擊
            self.driver.execute_script("arguments[0].click();", review_tab)
            
            # 等待評論區域載入
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"無法載入頁面或找不到評論按鈕: {url}")
            print(f"錯誤: {str(e)}")
            return False

    def click_sort_button(self):
        """點擊排序按鈕"""
        try:
            # 等待按鈕出現並可點擊
            sort_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="排序評論"]'))
            )
            
            # 確保按鈕在可視範圍內
            self.driver.execute_script("arguments[0].scrollIntoView(true);", sort_button)
            time.sleep(1)
            
            # 使用 JavaScript 點擊
            self.driver.execute_script("arguments[0].click();", sort_button)
            time.sleep(2)
            
            return True
        except Exception as e:
            print(f"點擊排序按鈕時發生錯誤: {str(e)}")
            return False

    def select_newest_first(self):
        """選擇最新排序選項"""
        try:
            # 等待排序選單出現
            time.sleep(2)
            
            # 使用更精確的選擇器來找到最新選項
            xpath_options = [
                # 嘗試通過完整的 class 結構找到元素
                "//div[contains(@class, 'twHv4e')]/div[contains(@class, 'mLuXec') and contains(text(), '最新')]",
                # 備選方案：直接找包含最新文字的 div
                "//div[contains(@class, 'mLuXec') and contains(text(), '最新')]",
                # 第三種嘗試：通過父元素的特定結構
                "//div[@role='menuitemradio']//div[contains(text(), '最新')]"
            ]
            
            newest_option = None
            for xpath in xpath_options:
                try:
                    newest_option = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    if newest_option:
                        break
                except:
                    continue
            
            if not newest_option:
                print("無法找到最新排序選項")
                return False
                
            # 嘗試將元素滾動到可見區域
            self.driver.execute_script("arguments[0].scrollIntoView(true);", newest_option)
            time.sleep(1)
            
            # 先嘗試一般的點擊
            try:
                newest_option.click()
            except:
                # 如果一般點擊失敗，使用 JavaScript 點擊
                try:
                    self.driver.execute_script("arguments[0].click();", newest_option)
                except:
                    # 如果直接點擊最新選項失敗，嘗試點擊父元素
                    parent = self.driver.execute_script("return arguments[0].parentNode;", newest_option)
                    self.driver.execute_script("arguments[0].click();", parent)
            
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"選擇最新排序時發生錯誤: {str(e)}")
            return False

    def scroll_reviews(self, target_review_count=20):
        """滾動載入評論直到達到目標數量"""
        try:
            reviews_div = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
            ))
            
            max_attempts = 10  # 最大滾動次數
            current_attempt = 0
            
            while current_attempt < max_attempts:
                # 檢查當前評論數量
                review_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.jJc9Ad')
                current_count = len(review_elements)
                
                print(f"已載入 {current_count} 則評論")
                
                if current_count >= target_review_count:
                    print("已達到目標評論數量")
                    break
                    
                # 滾動載入更多評論
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', reviews_div)
                time.sleep(2)
                current_attempt += 1
                
        except Exception as e:
            print(f"滾動載入評論時發生錯誤: {str(e)}")

    def get_store_name(self):
        """獲取店家名稱"""
        try:
            store_name = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'h1.DUwDvf')
            )).text
            return store_name
        except:
            return "Unknown Store"

    def extract_reviews(self, max_reviews=20):
        """提取評論內容，限制最大數量"""
        reviews = []
        try:
            review_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.jJc9Ad')
            
            # 只處理指定數量的評論
            for review in review_elements[:max_reviews]:
                try:
                    name = review.find_element(By.CSS_SELECTOR, 'div.d4r55').text
                    rating = len(review.find_elements(By.CSS_SELECTOR, 'span.kvMYJc img[src*="full_star"]'))
                    time_element = review.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
                    
                    try:
                        content = review.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                    except:
                        content = ""

                    reviews.append({
                        'store_name': self.get_store_name(),
                        'name': name,
                        'rating': rating,
                        'time': time_element,
                        'content': content
                    })
                except Exception as e:
                    print(f"提取單則評論時發生錯誤: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"提取評論時發生錯誤: {str(e)}")
            
        return reviews

    def save_to_csv(self, reviews, filename='google_maps_reviews.csv'):
        """將評論保存為 CSV 文件"""
        if reviews:
            df = pd.DataFrame(reviews)
            
            # 檢查文件是否已存在
            if os.path.exists(filename):
                # 如果存在，則附加到現有文件
                existing_df = pd.read_csv(filename)
                df = pd.concat([existing_df, df], ignore_index=True)
            
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"已保存 {len(reviews)} 則評論到 {filename}")
        else:
            print("沒有評論可保存")

    def close(self):
        """關閉瀏覽器"""
        self.driver.quit()

def main():
    scraper = GoogleMapsBatchScraper(headless=True)
    
    try:
        # 從 CSV 文件讀取 URL
        urls = scraper.load_urls_from_csv(['Louisa.csv', 'Cama.csv'])
        print(f"總共載入 {len(urls)} 個網址")
        
        all_reviews = []
        for i, url in enumerate(urls, 1):
            print(f"\n處理第 {i}/{len(urls)} 個網址: {url}")
            
            # 打開頁面
            if not scraper.open_page(url):
                continue
                
            # 點擊排序按鈕
            if not scraper.click_sort_button():
                continue
                
            # 選擇最新排序
            if not scraper.select_newest_first():
                continue
                
            # 滾動載入評論，目標20則
            scraper.scroll_reviews(target_review_count=20)
            
            # 提取最多20則評論
            reviews = scraper.extract_reviews(max_reviews=20)
            if reviews:
                all_reviews.extend(reviews)
                
            # 每處理 5 個網址就保存一次
            if i % 5 == 0:
                scraper.save_to_csv(all_reviews, 'coffee_shop_reviews.csv')
                
            time.sleep(3)  # 避免請求過於頻繁
            
        # 最後保存所有評論
        scraper.save_to_csv(all_reviews, 'coffee_shop_reviews.csv')
        
    except Exception as e:
        print(f"執行過程中發生錯誤: {str(e)}")
        
    finally:
        scraper.close()

if __name__ == "__main__":
    main()