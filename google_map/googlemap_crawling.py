from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time, random, os
from datetime import datetime

class GoogleMapsScraper:
    def __init__(self, output_file='comment', site_delay=(20, 40)):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu --no-sandbox --disable-dev-shm-usage --headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.output_file = f'{output_file}_{datetime.now().strftime("%Y%m%d")}.csv'
        self.site_delay = site_delay

    def load_urls_from_csv(self, *csv_files):
        return [(row['shop'], row['urls']) 
                for file in csv_files 
                for _, row in pd.read_csv(file).iterrows() 
                if str(row['urls']).startswith('http')]

    def click_review_tab(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[role="tab"][data-tab-index="1"]'))).click()
        time.sleep(2)
        sort_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='排序評論']")))
        self.driver.execute_script("arguments[0].click();", sort_btn)
        time.sleep(1)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='menuitemradio'][contains(., '最新')]"))).click()
        time.sleep(2)

    def scroll_reviews(self):
        div = self.driver.find_element(By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
        prev_count = 0
        
        for i in range(15):
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', div)
            time.sleep(random.uniform(2, 4))
            curr_count = len(self.driver.find_elements(By.CSS_SELECTOR, 'div.jftiEf'))
            print(f"已滾動 {i+1} 次")
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
                
                reviews.append({'store_name': store_name, 'rating': rating, 'content': content})
                processed_ids.add(review_id)
            except:
                continue
                
        return reviews

    def save_reviews(self, reviews):
        if not reviews:
            return
            
        df = pd.DataFrame(reviews)[['store_name', 'rating', 'content']]
        df.to_csv(self.output_file, mode='a', header=not os.path.exists(self.output_file), 
                 index=False, encoding='utf-8-sig')
        print(f"已儲存 {len(df)} 則評論")

    def scrape_reviews(self, *csv_files):
        try:
            for idx, (store_name, url) in enumerate(self.load_urls_from_csv(*csv_files), 1):
                print(f"\n進度: {idx}/{len(self.load_urls_from_csv(*csv_files))}")
                print(f"處理: {store_name}")
                
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    self.click_review_tab()
                    self.scroll_reviews()
                    self.save_reviews(self.extract_reviews(store_name))
                    
                    if idx < len(self.load_urls_from_csv(*csv_files)):
                        delay = random.uniform(*self.site_delay)
                        print(f"等待 {delay:.1f} 秒...")
                        time.sleep(delay)
                except:
                    print(f"處理 {store_name} 時發生錯誤")
                    continue
        finally:
            self.driver.quit()


if __name__ == "__main__":
    try:
        GoogleMapsScraper().scrape_reviews('Louisa.csv', 'Cama.csv')
    except KeyboardInterrupt:
        print("\n使用者中斷程式執行")
