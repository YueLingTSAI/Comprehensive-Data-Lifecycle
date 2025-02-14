from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import tempfile
import uuid
import datetime
from db_S import insert_data

class GoogleMapsScraper:
    def __init__(self, site_delay=(20, 40)):
        # 設定 Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-webgl')
        options.add_argument('--disable-webgl2')
        
        # 創建臨時目錄
        temp_dir = tempfile.mkdtemp()
        unique_id = str(uuid.uuid4())
        user_data_dir = f"{temp_dir}/chrome-data-{unique_id}"
        options.add_argument(f'--user-data-dir={user_data_dir}')
        
        try:
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            self.site_delay = site_delay
            self.url_counter = 0
            
        except Exception as e:
            print(f"Chrome 驅動程式初始化失敗: {str(e)}")
            raise

    def load_urls_from_csv(self, *csv_files):
        """從 CSV 讀取店鋪 URL"""
        urls = []
        for file in csv_files:
            try:
                df = pd.read_csv(file)
                for _, row in df.iterrows():
                    if str(row['urls']).startswith('http'):
                        urls.append((row['shop'], row['urls']))
            except Exception as e:
                print(f"載入 {file} 的 URL 時發生錯誤: {str(e)}")
        return urls

    def click_review_tab(self):
        """點擊評論標籤，設置最新排序"""
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[role="tab"][data-tab-index="1"]'))).click()
        time.sleep(2)
        
        sort_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@aria-label='排序評論']")))
        self.driver.execute_script("arguments[0].click();", sort_btn)
        time.sleep(1)
        
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@role='menuitemradio'][contains(., '最新')]"))).click()
        time.sleep(2)

    def scroll_reviews(self):
        """滾動載入評論"""
        div = self.driver.find_element(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
        prev_count = 0
            
        for i in range(1):
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', div)
            time.sleep(random.uniform(2, 4))
            curr_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'))
            print(f"已滾動 {i+1} 次")
            if curr_count == prev_count:
                break
            prev_count = curr_count

    def extract_reviews(self, store_name):
        """提取評論資料"""
        processed_ids = set()
        reviews = []
        review_count = 0
        
        for review in self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'):
            review_id = review.get_attribute('data-review-id')
            if review_id in processed_ids:
                continue
                
            try:
                try:
                    content = review.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                except:
                    content = ""
                
                rating = sum(1 for star in review.find_elements(By.CSS_SELECTOR, 'span.hCCjke') 
                        if 'elGi1d' in star.get_attribute('class'))
                
                brand = "Louisa" if self.url_counter < 50 else "Cama"
                content_time = review.find_element(By.CSS_SELECTOR, 'span.rsqaWe').text
                crawling_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                review_data = {
                    'brand': brand,
                    'store_name': store_name,
                    'rating': rating,
                    'content': content,
                    'content_time': content_time,
                    'crawling_time': crawling_time
                }
                
                reviews.append(review_data)
                processed_ids.add(review_id)
                review_count += 1
                
            except Exception as e:
                print(f"\n解析評論時發生錯誤: {str(e)}")
                continue
        
        # 立即儲存評論到資料庫
        if reviews:
            insert_data(reviews)

    def scrape_reviews(self, *csv_files):
        """執行爬蟲主程式"""
        urls = self.load_urls_from_csv(*csv_files)
        if not urls:
            print("CSV 檔案中沒有有效的網址")
            return
            
        try:
            total_urls = len(urls)
            for idx, (store_name, url) in enumerate(urls, 1):
                print(f"\n進度: {idx}/{total_urls}")
                print(f"處理: {store_name}")
                
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    
                    self.click_review_tab()
                    self.scroll_reviews()
                    self.extract_reviews(store_name)
                    
                    self.url_counter += 1
                    
                    if idx < total_urls:
                        delay = random.uniform(*self.site_delay)
                        print(f"等待 {delay:.1f} 秒...")
                        time.sleep(delay)
                except Exception as e:
                    print(f"處理 {store_name} 時發生錯誤: {str(e)}")
                    continue
                    
        finally:
            self.driver.quit()

if __name__ == "__main__":
    try:
        scraper = GoogleMapsScraper()
        scraper.scrape_reviews('Louisa.csv', 'Cama.csv')
    except KeyboardInterrupt:
        print("\n使用者中斷程式執行")