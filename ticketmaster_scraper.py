from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

URL = "https://www.ticketmaster.es/artist/ariana-grande-entradas/882826?startDate=2026-08-15&endDate=2026-09-01"

def check_ticketmaster():
    """
    Checks for ticket availability on Ticketmaster by navigating through events.

    Returns:
        (bool, str): A tuple containing True and the event URL if tickets are available, 
                     otherwise (False, None).
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    driver = None
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(URL)

        # Wait for event listings to be present
        WebDriverWait(driver, 20).until(
             EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='event-list-link']"))
        )
        time.sleep(2) # allow for dynamic content to load

        event_buttons = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='event-list-link']")
        event_urls = [btn.get_attribute('href') for btn in event_buttons if btn.get_attribute('href')]

        if not event_urls:
            print("Ticketmaster: No event links found.")
            return False, None

        for event_url in event_urls:
            try:
                # Navigate to the event page directly
                driver.get(event_url)
                time.sleep(2) # Wait for page to load

                # Check for the 'no results' message
                page_source = driver.page_source.lower()
                if "sorry, we couldn't find any results" in page_source or "Sorry, we couldn't find any results" in page_source:
                    print(f"Ticketmaster: No tickets for {event_url}")
                    continue
                else:
                    print(f"Ticketmaster: Tickets might be available at {event_url}")
                    return True, event_url

            except (TimeoutException, NoSuchElementException) as e:
                print(f"An error occurred while checking {event_url}: {e}")
                continue

        print("Ticketmaster: No tickets found in any event.")
        return False, None

    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    available, url = check_ticketmaster()
    if available:
        print(f"Tickets found at: {url}")
