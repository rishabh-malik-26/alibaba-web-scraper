
import time


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














