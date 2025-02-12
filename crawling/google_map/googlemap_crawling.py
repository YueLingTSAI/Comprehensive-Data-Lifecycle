from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db import insert_data, show_data  # 引入資料庫函式
import pandas as pd
import time
import random
import os
import tempfile
import uuid

class GoogleMapsScraper:
    def __init__(self, site_delay=(20, 40)):
        # Chrome options setup
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        
        # Setting up unique user data directory
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
            print(f"Chrome driver initialization failed: {str(e)}")
            raise

    def load_urls_from_csv(self, *csv_files):
        urls = []
        for file in csv_files:
            try:
                df = pd.read_csv(file)
                for _, row in df.iterrows():
                    if str(row['urls']).startswith('http'):
                        urls.append((row['shop'], row['urls']))
            except Exception as e:
                print(f"Error loading URLs from {file}: {str(e)}")
        return urls

    def click_review_tab(self):
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
        div = self.driver.find_element(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
        prev_count = 0
            
        for i in range(15):
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', div)
            time.sleep(random.uniform(2, 4))
            curr_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'))
            print(f"Scrolled {i+1} times")
            if curr_count == prev_count:
                break
            prev_count = curr_count
        

    def extract_reviews(self, store_name):
        processed_ids = set()
        reviews = []
        
        for review in self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'):
            review_id = review.get_attribute('data-review-id')
            if review_id in processed_ids:
                continue
                
            try:
                content = review.find_element(By.CSS_SELECTOR, 'span.wiI7pd').text
                if not content.strip():
                    continue
                
                rating = sum(1 for star in review.find_elements(By.CSS_SELECTOR, 'span.hCCjke') 
                           if 'elGi1d' in star.get_attribute('class'))
                
                brand = "Louisa" if self.url_counter < 50 else "Cama"
                
                reviews.append({
                    'brand': brand,
                    'store_name': store_name,
                    'rating': rating,
                    'content': content
                })
                processed_ids.add(review_id)
            except:
                continue
                
        return reviews

    def save_reviews(self, reviews):
        insert_data(reviews)

    def scrape_reviews(self, *csv_files):
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
                    reviews = self.extract_reviews(store_name)
                    self.save_reviews(reviews)
                    
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

    def __del__(self):
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
        except:
            pass
        finally:
            # 清理殘留進程
            os.system('pkill -f chrome')
            os.system('pkill -f chromedriver')

if __name__ == "__main__":
    try:
        GoogleMapsScraper().scrape_reviews('Louisa.csv', 'Cama.csv')
        show_data
    except KeyboardInterrupt:
        print("\n使用者中斷程式執行")