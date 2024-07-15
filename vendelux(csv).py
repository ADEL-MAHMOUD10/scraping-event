from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

browser = webdriver.Firefox()
browser.implicitly_wait(2)

for i in range(1, 11):
    url = 'https://vendelux.com/app/events/search?page=' + str(i)
    browser.get(url)
    
    names = browser.find_elements(By.CSS_SELECTOR, 'h6.MuiTypography-root')
    dates = browser.find_elements(By.CSS_SELECTOR, 'span.MuiTypography-root')
    locations = browser.find_elements(By.CSS_SELECTOR, '.MuiStack-root :nth-child(1) p')
    prices = browser.find_elements(By.CSS_SELECTOR, '.MuiStack-root :nth-child(3) p')

    for name, date, location , price  in zip(names, dates, locations, prices):
        print(f"scraped from page {i} - Event: {name.text.strip()}")
        print(f"scraped from page {i} - date: {date.text.strip()}")
        print(f"scraped from page {i} - location: {location.text.strip()}")
        print(f"scraped from page {i} - price: {price.text.strip()}")
        event_info = {"Page Number": i ,"Event": name.text.strip(), "Date": date.text.strip(), "Location": location.text.strip(), "Price": price.text.strip()}
        with open("vendelux.csv", 'a', newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["Page Number" ,"Event", "Date", "Location", "Price"])
            # Write the header only if the file is empty
            if not csv_file.tell():
                writer.writeheader()

            # Write each event data to the CSV file
            writer.writerow(event_info)

print("Finished scraping!")
# Close the browser after scraping (important)
browser.quit()
