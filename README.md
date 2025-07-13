# Alibaba RFQ Scraper 🚀

This project is a **web scraper** built with **Playwright** (Python) to extract **Request for Quotation (RFQ)** data from [sourcing.alibaba.com](https://sourcing.alibaba.com/).  
It navigates RFQ listing pages, scrapes detailed buyer info, and saves the data to a CSV for further analysis or automation.

---

## 📌 **Features**

- Extracts key RFQ details:
  - RFQ headings
  - Quantity required
  - Buyer name & country
  - Quotes left
  - Inquiry time (converted to absolute date)
  - Inquiry URLs & unique UUIDs
  - Buyer tags (one-hot encoded as yes/no)
  - Buyer images
  - Scraping timestamp
- Handles pagination automatically.
- Supports structured DataFrame output (CSV).
- Uses `Playwright` for robust headless scraping.

---

## ⚙️ **Project Structure**

---

## 🚀 **How it works**

1. Starts with an RFQ listing page URL.
2. Loads all RFQ items on the page.
3. Extracts relevant fields.
4. Adds scraping timestamp.
5. Repeats for next pages using pagination links.
6. Outputs final data to a CSV file.

---

## 🗃️ **Output Columns**

| Column          | Description                          |
|-----------------|--------------------------------------|
| quantity        | Required quantity for the RFQ        |
| headings        | RFQ title / product name             |
| buyer_names     | Name of the buyer                    |
| countries       | Buyer country                        |
| quotes_left     | How many quotes left                 |
| inquiry_time    | Date/time when the inquiry was posted|
| inquiry_urls    | Direct link to the RFQ detail page   |
| rfq_uuid        | Unique ID extracted from the URL     |
| tags            | Buyer tags one-hot encoded (yes/no)  |
| images          | Buyer profile image link (if available) |
| scrape_date     | Datetime when the scrape ran         |

---

## ✅ **How to Run**

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
2. ** Run main.py **
