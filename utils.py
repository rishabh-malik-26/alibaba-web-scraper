import time
from datetime import datetime
import dateparser
from urllib.parse import urlparse, parse_qs


def get_h1(page) -> list:

    all_headings = []
    page.wait_for_selector("h1")
    headings = page.query_selector_all("h1")
    for heading in headings:
        if heading:
            all_headings.append(heading.text_content().strip())
        else:
            all_headings.append(None)

    return all_headings


def buyer_name(page):
    all_buyer_names = []
    buyer_name_elements = page.wait_for_selector('div.text')
    time.sleep(3)
    buyer_namesnames = page.query_selector_all("div.text")
    for name in buyer_namesnames:

        if name:
            all_buyer_names.append(name.text_content().strip())
        else:
            all_buyer_names.append(None)
    
    return all_buyer_names


def get_quotes_left(page):
    all_quotes_left = []
    quotes_left_elements = page.wait_for_selector('div.brh-rfq-item__quote-left')

    time.sleep(3)
    quotes = page.query_selector_all("div.brh-rfq-item__quote-left")

    for quote in quotes:

        if quote:
            all_quotes_left.append(quote.text_content().strip())
        else:
            all_quotes_left.append(None)

    return all_quotes_left



def get_country(page):

    country_elements = page.wait_for_selector('div.brh-rfq-item__country')
    time.sleep(3)
    
    all_countries = []
    country_divs = page.query_selector_all("div.brh-rfq-item__country")

    for div in country_divs:
        country_name = None

        # Try to get from <img> title first
        flag_img = div.query_selector("img.brh-rfq-item__country-flag")
        if flag_img:
            country_name = flag_img.get_attribute("title")
        
        # Fallback: use the text node if title is missing or empty
        if not country_name:
            full_text = div.text_content().strip()
            
            # Remove label text if it exists
            label = div.query_selector("span.brh-rfq-item__label")
            if label:
                label_text = label.text_content().strip()
                full_text = full_text.replace(label_text, "").strip()
            
            country_name = full_text

        all_countries.append(country_name)
    
    return all_countries




def get_quantity_required(page):

    all_quantities = []

    quantity_element = page.wait_for_selector("div.brh-rfq-item__quantity")
    time.sleep(3)

    quantity_divs  = page.query_selector_all("div.brh-rfq-item__quantity")

    for div in quantity_divs:

        whole_text = div.text_content().strip()

        label_span = div.query_selector("span")

        label_text = ""
        if label_span:
            label_text = label_span.text_content().strip()

        raw_text = whole_text.replace(label_text, "").strip()

        all_quantities.append(raw_text)
         
    return all_quantities
 

def get_inquiry_time(page):
        all_date_posted = []

        inquiry_date_element = page.wait_for_selector('div.brh-rfq-item__publishtime')
        time.sleep(3)

        date_divs = page.query_selector_all('div.brh-rfq-item__publishtime')

        for div in date_divs:

            full_text = div.text_content().strip()

            span = div.query_selector("span.brh-rfq-item__label")
            
            if span:
                span_text  = span.text_content().strip()

            outside_text = full_text.replace(span_text, "").strip()

            all_date_posted.append(outside_text)

        return all_date_posted


def get_inquiry_urls(page):

    all_inquiry_urls = []

    inquiry_url_element = page.wait_for_selector('h1.brh-rfq-item__subject')
        # time.sleep(3)

    url_divs = page.query_selector_all('h1.brh-rfq-item__subject')

    for div in url_divs:
        a_tag =div.query_selector("a.brh-rfq-item__subject-link")

        if a_tag:
            href = a_tag.get_attribute("href")
            all_inquiry_urls.append(href)
        else:
            all_inquiry_urls.append(None)

    return all_inquiry_urls



def get_buyer_tags(page):

    buyer_tags = []
        # Get all main RFQ info blocks
    rfq_infos = page.query_selector_all('div.brh-rfq-item__other-info')

    for rfq in rfq_infos:
        buyer_flag_div = rfq.query_selector('div.bc-brh-rfq-flag--buyer')

        if buyer_flag_div:
            tags_divs_inner = buyer_flag_div.query_selector_all("div.next-tag-zoom-appear-active")

            if tags_divs_inner:
                separate_tags = []
                for td in tags_divs_inner:
                    if td:
                        sub_div = td.query_selector("div.next-tag-body")
                        if sub_div:
                            div_text = sub_div.text_content().strip()
                            separate_tags.append(div_text)
                        else:
                            separate_tags.append([])
                    else:
                        separate_tags.append([])
                buyer_tags.append(separate_tags)
            else:
                buyer_tags.append([])
        else:
            buyer_tags.append([])
    
    return buyer_tags


def get_buyer_image(page):
    all_images = []  

    image_div_element = page.wait_for_selector('div.avatar')

    image_divs = page.query_selector_all("div.avatar")

    for div in image_divs:
        if div:
            image_tag = div.query_selector('img')
            if image_tag:
                image = image_tag.get_attribute('src')
                all_images.append(image)
            else:
                all_images.append(None)
        else:
            all_images.append(None)
    
    return all_images




def get_next_page(page):
            

        try:
            # Wait for the pagination container to appear
            page.wait_for_selector("div.ui2-pagination-pages", timeout=5000)

            pagination_div = page.query_selector("div.ui2-pagination-pages")
            if not pagination_div:
                return None  # Could not find pagination block

            next_page = pagination_div.query_selector("a.next")
            if next_page:
                href = next_page.get_attribute("href")
                if href:
                    if href.startswith("//"):
                        href = "https:" + href
                    elif href.startswith("/"):
                        href = "https://sourcing.alibaba.com" + href
                    return href
            return None  # No next link found

        except Exception as e:
            return str(e)  # Safer to return str instead of raw Exception

from sklearn.preprocessing import MultiLabelBinarizer
import pandas as pd

def tags_to_df(b_tags):

    mlb = MultiLabelBinarizer()

    one_hot = mlb.fit_transform(b_tags)

    tags_df = pd.DataFrame(one_hot, columns=mlb.classes_)

    tags_df = tags_df.astype(int)

    new_df = tags_df.replace({1: 'yes', 0: 'no'})

    return new_df




def convert_relative_time(text):
    now = datetime.now()

    parsed_dt = dateparser.parse(
        text,
        settings={'RELATIVE_BASE': now}
    )

    if parsed_dt:
        return parsed_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None



def get_inquiry_date(page):
        
        all_date_posted = []

        inquiry_date_element = page.wait_for_selector('div.brh-rfq-item__publishtime')
        time.sleep(3)

        date_divs = page.query_selector_all('div.brh-rfq-item__publishtime')

        for div in date_divs:

            full_text = div.text_content().strip()

            span = div.query_selector("span.brh-rfq-item__label")
            
            if span:
                span_text  = span.text_content().strip()

            outside_text = full_text.replace(span_text, "").strip()

            date = convert_relative_time(outside_text)

            all_date_posted.append(date)

        return all_date_posted



def get_rfq_uuid_from_url(url):
    """
    Takes a single RFQ detail page URL and returns the UUID.
    If not found, returns None.
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    uuid = qs.get('uuid', [None])[0]
    return uuid


def get_rfq(page):
    
    page.wait_for_selector('a.brh-rfq-item__subject-link')

    subject_links = page.query_selector_all('a.brh-rfq-item__subject-link')

    all_rfqs = []
    for link in subject_links:
        href = link.get_attribute('href')
        if href:
            if href.startswith('//'):  # Alibaba uses protocol-relative URLs
                href = 'https:' + href
                rfq = get_rfq_uuid_from_url(href)
            all_rfqs.append(rfq)
        else:
            all_rfqs.append(None)

    return all_rfqs

