from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from webdriver_manager.chrome import ChromeDriverManager


# Set up Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection


# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# Open Product Hunt Leaderboard page
url = "https://www.producthunt.com/leaderboard/yearly/2025/all"
driver.get(url)


# Wait until at least one company listing is visible
try:
   WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, "text-16.font-semibold"))
   )
   print("Page loaded successfully!")
except Exception as e:
   print("Page didn't load correctly. Error:", e)
   driver.quit()
   exit()


# Scroll to load more startups dynamically
for _ in range(5):  # Adjust based on how many startups you want
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   time.sleep(2)


# Extract Data using Selenium
startups = []
company_elements = driver.find_elements(By.CLASS_NAME, "text-16.font-semibold")  # Company name elements


for company in company_elements:
   try:
       name = company.text.strip()
   except:
       name = "N/A"


   try:
       description = company.find_element(By.XPATH, "./following-sibling::a[contains(@class, 'text-16 font-normal text-dark-gray text-secondary')]").text.strip()
   except:
       description = "N/A"


   try:
       website_tag = company.find_element(By.XPATH, "./ancestor::section[1]//a")
       website = website_tag.get_attribute("href") if website_tag else "N/A"
   except:
       website = "N/A"


   startups.append({"Name": name, "Description": description, "Website": website})


# Close Selenium session
driver.quit()


# Save to JSON file
with open("producthunt_startups.json", "w", encoding="utf-8") as json_file:
   json.dump(startups, json_file, indent=4, ensure_ascii=False)


print("Scraping complete. Data saved to producthunt_startups.json")