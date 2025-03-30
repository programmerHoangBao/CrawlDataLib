from service.RequestWebsite import CrawlData
import service.FileTextService as FileTextService
import re


def standardize_currency(input_str):
    """
    Standardizes a currency string into an integer.
    
    :param input_str: The input currency string (e.g., "9.490.000đ")
    :return: An integer representing the standardized value (e.g., 9490000)
    """
    # Remove dots, commas, and non-digit characters using regular expressions
    standardized_str = re.sub(r'[^\d]', '', input_str)
    return int(standardized_str)

def extract_ram_value(input_str):
    """
    Extracts the numeric value of RAM from a given string.
    
    :param input_str: The input string (e.g., "RAM: 8 GB")
    :return: The extracted numeric value as an integer (e.g., 8)
    """
    match = re.search(r'\d+', input_str)  # Search for the first numeric sequence in the string
    if match:
        return int(match.group())
    else:
        raise ValueError("No numeric value found in the input string.")




def main():
    url = "https://www.thegioididong.com/dtdd-samsung#c=42&m=2&o=13&pi=1"
    selector_ul = "#categoryPage > div.container-productbox > ul"

    # Retrieve page source using Selenium
    page_source = CrawlData.get_page_source_selenium(url)

    # CSS selectors for product details
    n = 9
    products = []
    selector_li = ""
    selector_name = ""
    selector_current_price = ""
    selector_old_price = ""
    selector_RAM = ""

    # Loop to process multiple products
    for i in range(1, n + 1):
        selector_li = f"#categoryPage > div.container-productbox > ul > li:nth-child({i})"
        selector_name = f"{selector_li} > a > h3"
        selector_current_price = f"{selector_li} > a > strong"
        selector_old_price = f"{selector_li} > a > div.box-p > p"
        selector_RAM = f"{selector_li} > div.utility > p:nth-child(2)"

        # Extract product details using CrawlData methods
        id = CrawlData.get_attribute_value(page_source, selector_li, "data-id").pop()
        name = CrawlData.get_attribute_value(page_source, selector_name).pop()
        current_price = standardize_currency(CrawlData.get_attribute_value(page_source, selector_current_price).pop())
        old_price = standardize_currency(CrawlData.get_attribute_value(page_source, selector_old_price).pop())
        ram = extract_ram_value(CrawlData.get_attribute_value(page_source, selector_RAM).pop())

        # Format result and save to TXT file
        result = f"({id},{name},{current_price},{old_price},{ram})"
        if FileTextService.check_txt_file_exists("samsung.txt"):
            FileTextService.add_data_to_txt_file("samsung.txt", result)
        else:
            FileTextService.create_txt_file("samsung.txt", result)

if __name__ == "__main__":
    main()
