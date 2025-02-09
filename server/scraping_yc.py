from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import json

# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define function to scrape startup listings
def scrape_wellfound(url, max_pages=5):
    driver.get(url)
    time.sleep(5)  # Allow time for JavaScript to load
    
    startups = []
    
    for _ in range(max_pages):
        # Extract startup listings
        listings = driver.find_elements(By.CLASS_NAME, "_company_1pgsr_355")  # Adjust class as needed
        
        for listing in listings:
            try:
                name = listing.find_element(By.CLASS_NAME, "_coName_1pgsr_470").text
                # industry = listing.find_element(By.CLASS_NAME, "_tagLink_1pgsr_1040").text
                industry = listing.find_elements(By.XPATH, "//a[contains(@href, 'industry=')]/span")
                # funding = listing.find_element(By.CLASS_NAME, "styles_funding__2yxgU").text
                startups = [element.text for element in industry]
                # ind = [element.text for element in industry]
                # startups.append([industry])
            except:
                continue

        # Scroll down and load more
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    return pd.DataFrame(startups, columns=["Industry"])

# Scrape data
url = "https://www.ycombinator.com/companies"  # Adjust based on your search criteria
df = scrape_wellfound(url, max_pages=3)

json_data = df.to_dict(orient="records")
with open("companies.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)