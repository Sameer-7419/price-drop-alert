import schedule
import time
import requests
from bs4 import BeautifulSoup
import smtplib
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import random
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# ----------------- Configuration -----------------
PRODUCT_URL = os.getenv('YOUR_PRODUCT_URL')
TARGET_PRICE = int(os.getenv('TARGET_PRICE'))
YOUR_EMAIL = os.getenv('YOUR_EMAIL')
APP_PASSWORD = os.getenv('YOUR_EMAIL_PASSWORD')
TO_EMAIL = os.getenv('YOUR_TO_EMAIL')

HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})
# --------------------------------------------------

def get_price():
    options = Options()
    options.add_argument('--headless')  # Run in background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(PRODUCT_URL)
        time.sleep(random.uniform(3, 6))  # Random delay
        
        # Get title
        title_element = driver.find_element(By.ID, "productTitle")
        product_title = title_element.text.strip()
        
        # Get price
        price_elements = driver.find_elements(By.CSS_SELECTOR, "span.a-price-whole")
        for element in price_elements:
            price_text = element.text.strip()
            if price_text and price_text.replace(',', '').isdigit():
                current_price = float(price_text.replace(',', ''))
                return product_title, current_price
        
        return None, None
        
    except Exception as e:
        print(f"Selenium error: {e}")
        return None, None
    finally:
        driver.quit()
        
        
def send_email(product_title, current_price):
        subject = f"🔔 Price Drop: ₹{current_price} for '{product_title[:50]}...'"
        body = f"The price has dropped to ₹{current_price}!\n\nCheck it out here: {PRODUCT_URL}"
        message = f"Subject: {subject}\n\n{body}".encode('utf-8')

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(YOUR_EMAIL, APP_PASSWORD)
                server.sendmail(YOUR_EMAIL, TO_EMAIL, message)
            print("✅ Email sent successfully.")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")


def job():
    product_title, current_price = get_price()
    if product_title and current_price:
        print(f"🛍️ {product_title} - Current Price: ₹{current_price}")
        if current_price < TARGET_PRICE:
            print(f"✅ Price is below ₹{TARGET_PRICE}. Sending email...")
            send_email(product_title, current_price)
        else:
            print(f"⏳ Price is above ₹{TARGET_PRICE}. No email sent.")


# Schedule the job every 12 hours
schedule.every(12).hours.do(job)

print("📅 Price alert script running... Press Ctrl+C to stop.")
job()  # Run once at start

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every 60 seconds if a task is due
