from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize the driver with webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# List of URLs to scrape
urls = [
    "https://www.ycombinator.com/companies/coinbase",
    "https://www.ycombinator.com/companies/airbnb",
    "https://www.ycombinator.com/companies/dropbox",
    "https://www.ycombinator.com/companies/amplitude",
    "https://www.ycombinator.com/companies/doordash",
    "https://www.ycombinator.com/companies/ginkgo-bioworks",
    "https://www.ycombinator.com/companies/gitlab",
    "https://www.ycombinator.com/companies/instacart"
    # Add more URLs as needed
]

# This list will hold the scraped data for all companies
companies_data = []

try:
    for url in urls:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        try:
            # Extract company name using CSS selector for multiple classes
            name = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".text-3xl.font-bold")
            )).text
            
            # Extract company description
            description = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".prose.max-w-full.whitespace-pre-line")
            )).text
            
            
            # Append the scraped data for this company as a dictionary
            companies_data.append({
                "name": name,
                "description": description
            })
            print(f"Scraped data from {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            
    # Save all scraped data into a JSON file
    with open("companies_data.json", "w", encoding="utf-8") as f:
        json.dump(companies_data, f, indent=2)
    print("All data saved to companies_data.json")

except Exception as e:
    print(f"An error occurred during scraping: {e}")

finally:
    driver.quit()
