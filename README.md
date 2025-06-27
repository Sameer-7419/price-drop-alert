# 🛒 Amazon Price Tracker Bot (with Email Alerts)

This Python script tracks the price of an Amazon product and sends you an email alert when the price drops below your desired value.

---

## 📦 Features

- ✅ Real-time price scraping with **Selenium**
- 📬 Sends **email alerts** using Gmail SMTP
- ⏰ **Runs automatically every 12 hours** with `schedule`
- 🔐 Configuration using a `.env` file (no hardcoding sensitive info)

---

## 🧾 Code Summary

### Main Components:
- **`get_price()`** – Uses Selenium to extract product title and price.
- **`send_email()`** – Sends an email notification when price drops.
- **`job()`** – Scheduled job that checks the price and triggers email if needed.

### Libraries Used:
- `selenium`, `smtplib`, `schedule`, `dotenv`, `requests`, `BeautifulSoup`, `webdriver-manager`

---

## ⚙️ Setup Instructions

### Clone the Repository , Install the dependencies And Run the script

```bash
git clone https://github.com/Sameer-7419/price-drop-alert.git
cd price-drop-alert
pip install selenium schedule requests beautifulsoup4 python-dotenv webdriver-manager
python notify.py
