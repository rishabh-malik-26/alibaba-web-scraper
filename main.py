from playwright.sync_api import sync_playwright
from utils import *
import logging
from datetime import  datetime
import pandas as pd
logging.basicConfig(level=logging.INFO,format= '%(asctime)s - %(levelname)s - %(message)s')


def extract_data(page):

        try:

            scrape_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            images = get_buyer_image(page=page)

            tags = get_buyer_tags(page=page)

            inquiry_urls = get_inquiry_urls(page=page)

            inquiry_time = get_inquiry_time(page=page)

            quantity = get_quantity_required(page=page)

            headings = get_h1(page=page)

            buyer_names = buyer_name(page=page)

            countries = get_country(page=page)
            
            quotes_left = get_quotes_left(page=page)

            inquiry_date = get_inquiry_date(page=page)

            rfgs = get_rfq(page=page)

            data = {
                'quantity': quantity,
                'headings': headings,
                'buyer_names': buyer_names,
                'countries': countries,
                'quotes_left': quotes_left,
                'inquiry_time': inquiry_time,
                'inquiry_urls': inquiry_urls,
                'images': images,
                'inquiry_date':inquiry_date,
                'rfqs':rfgs,
                'scrape_date': [scrape_datetime] * len(quantity)  # Repeat for each row!

            }

            df = pd.DataFrame(data)

            buyer_tag_df = tags_to_df(tags)            
            
            df = pd.concat([df,buyer_tag_df],axis= 1)

            return df

        except Exception as e:
            print(f'Error Occured:{e}')


url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&tracelog=newest"


## Pipeline
master_df = pd.DataFrame()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)

    while url:
        print(f"Scraping: {url}")
        page.goto(url)
        
        df = extract_data(page)
        master_df = pd.concat([master_df, df], ignore_index=True)

        master_df.to_csv("alibaba_rfqs.csv", index=False)

        url = get_next_page(page)

    browser.close()


print("Scraping finished. Total rows:", len(master_df))









