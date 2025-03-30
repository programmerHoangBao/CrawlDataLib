from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class CrawlData:

    @staticmethod
    def simulate_click_XPATH(URL, XPATH, wait_time=10, driver=None, headless=False, time_sleep=0.5):
        if driver is None:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)

        page_source = None
        try:
            driver.get(URL)
            click_even = WebDriverWait(driver=driver, timeout=wait_time).until(
                EC.element_to_be_clickable((By.XPATH, XPATH))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click_even)
            driver.execute_script("arguments[0].click();", click_even)
            time.sleep(time_sleep)
            page_source = driver.page_source
        except Exception as e:
            print(f"Error: {e}")
        finally:
            driver.quit()
        return page_source
    
    @staticmethod
    def simulate_click_selector(URL, selector, wait_time=10, driver=None, headless=False, time_sleep=0.5):
        if driver is None:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)

        page_source = None
        try:
            driver.get(URL)
            click_even = WebDriverWait(driver=driver, timeout=wait_time).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", click_even)
            driver.execute_script("arguments[0].click();", click_even)
            time.sleep(time_sleep)
            page_source = driver.page_source
        except Exception as e:
            print(f"Error: {e}")
        finally:
            driver.quit()
        return page_source
    
    @staticmethod
    def get_attribute_value(page_source, selector, attribute="text", base_url=""):
        soup = BeautifulSoup(page_source, "html.parser")
        elements = soup.select(selector)

        if not elements:
            return set()

        attr_values = set()

        for element in elements:
            if attribute.lower() == "text":
                attr_values.add(element.get_text(strip=True))
            else:
                attr_value = element.get(attribute) if element.has_attr(attribute) else None
                if attribute.lower() == "href" and attr_value:
                    parsed_url = urlparse(attr_value)
                    if not parsed_url.netloc:
                        attr_value = urljoin(base_url, attr_value)
                if attr_value:
                    attr_values.add(attr_value)

        return attr_values


    @staticmethod
    def get_attribute_value_with_selenium(url, selector, attribute="text", by=By.CSS_SELECTOR, driver=None, headless=False):
        should_quit = False

        if driver is None:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            should_quit = True

        result = set()

        try:
            driver.get(url)
            elements = driver.find_elements(by, selector)
            for element in elements:
                if attribute.lower() == "text":
                    value = element.text.strip() if element.text else None
                else:
                    value = element.get_attribute(attribute) if element else None

                if value:
                    result.add(value)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if should_quit:
                driver.quit()

        return result
        
    @staticmethod
    def get_child_selectors(page_source, selector):
        soup = BeautifulSoup(page_source, "html.parser")
        parent = soup.select_one(selector)

        if not parent:
            return set()

        child_selectors = set()
        for child in parent.find_all(recursive=False):
            tag_name = child.name
            class_name = ".".join(child.get("class", []))
            id_name = child.get("id")

            child_selector = f"{selector} > {tag_name}"
            if id_name:
                child_selector += f"#{id_name}"
            elif class_name:
                child_selector += f".{class_name}"

            child_selectors.add(child_selector)

        return child_selectors

    
    @staticmethod
    def get_child_selectors_with_selenium(url, selector, by=By.CSS_SELECTOR, driver=None, headless=False):
        should_quit = False

        if driver is None:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            should_quit = True

        result = set()

        try:
            driver.get(url)
            parent = driver.find_element(by, selector)
            if parent:
                child_elements = parent.find_elements(By.XPATH, "./*")
                child_selectors = set()

                for child in child_elements:
                    tag_name = child.tag_name
                    class_name = ".".join(child.get_attribute("class").split()) if child.get_attribute("class") else ""
                    id_name = child.get_attribute("id")

                    child_selector = f"{selector} > {tag_name}"
                    if id_name:
                        child_selector += f"#{id_name}"
                    elif class_name:
                        child_selector += f".{class_name}"

                    child_selectors.add(child_selector)

                result = child_selectors

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if should_quit:
                driver.quit()

        return result

    
    @staticmethod
    def get_page_source_selenium(url, headless=True):
        """
        Fetches the page source of a website using Selenium.
    
        :param url: The URL of the website
        :param headless: Whether to run the browser in headless mode
        :return: The page source (HTML) as a string
        """
        options = Options()
        if headless:
            options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Initialize the WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
        try:
            driver.get(url)
            page_source = driver.page_source  # Get the HTML source code
        finally:
            driver.quit()  # Close the browser

        return page_source
    
    @staticmethod
    def get_child_selectors_by_tag(page_source, parent_selector, child_tag, child_class=None):
        """
        The function of extracting the selector of the sub -attribute from a parent attribute
        Args:
            page_source (str): Source HTML of the website.
            parent_selector (str): Selector of Cha.
            child_tag (str): The HTML card I need to take (for example: 'Li', 'A', ...).
            child_class (str): (No required) Class of the sub -attribute.

        Returns:
            List of selectors of sub -attributes.
        """
        soup = BeautifulSoup(page_source, 'html.parser')
        parent_element = soup.select_one(parent_selector)
        if not parent_element:
            raise ValueError("The father's element was not found with Selector.")
    
        if child_class:
            child_elements = parent_element.find_all(child_tag, class_=child_class)
        else:
            child_elements = parent_element.find_all(child_tag)
    
        selectors = []
        for element in child_elements:
            selector = f"{child_tag}"
            if 'class' in element.attrs:
                class_name = "." + ".".join(element['class'])
                selector += class_name
            selectors.append(selector)
    
        return selectors
    
    @staticmethod
    def check_selector_exists(page_source, selector):
        """
        Check if Selector exists on the website.

        Args:
            page_source (str): Source HTML of the website.
            selector (str): Selector needs to check.

        Returns:
            bool: True if Selector exists, False otherwise.
        """
        soup = BeautifulSoup(page_source, 'html.parser')
        element = soup.select_one(selector)
        return element is not None


