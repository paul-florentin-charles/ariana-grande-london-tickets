from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time

URL = "https://www.axs.com/uk/series/29116/ariana-grande-at-the-o2-the-eternal-sunshine-tour-tickets?skin=theo2"

def check_axs():
    """
    Checks for ticket availability on AXS.

    Returns:
        (bool, str): A tuple containing True and the event URL if tickets are available, 
                     otherwise (False, None).
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(URL)

        # 1. Collect all event URLs first
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='CTAButton']"))
        )
        time.sleep(2) # Allow extra time for JS to render

        event_buttons = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='CTAButton']")
        urls = [btn.get_attribute('href') for btn in event_buttons if btn.get_attribute('href')]

        if not urls:
            print("AXS: No event links found.")
            return False, None

        print(f"AXS: Found {len(urls)} events to check.")

        # 2. Now, iterate through the collected URLs
        for event_url in urls:
            event_url = event_url.split("?")[0] + "/ariana-grande-tickets"
            print(event_url)
            try:
                driver.get(event_url)
                time.sleep(3)

                # Wait for the 'Get Tickets' link to be present
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Get Tickets - Tickets"]'))
                )

                # Extract href link and use it for getting availability
                get_tickets_links = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Get Tickets - Tickets"]')
                driver.get(get_tickets_links[0].get_attribute('href'))

                # Wait for the new page to load
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(3) # Allow extra time for any redirects or JS rendering

                page_source = driver.page_source.lower()
                if "sales have ended" in page_source or "tickets are not currently available" in page_source:
                    print(f"AXS Event ({event_url}): Sales have ended or tickets are unavailable.")
                    continue # Just go to the next URL in the list
                else:
                    print(f"AXS Event ({driver.current_url}): Tickets might be available!")
                    return True, driver.current_url

            except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
                print(f"Could not process event {event_url}: {e}")
                continue # Continue to the next URL

        print("AXS: No tickets found across all checked events.")
        return False, None

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    available, url = check_axs()
    if available:
        print(f"Tickets found at: {url}")
