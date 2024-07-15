from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3

browser = webdriver.Firefox()
browser.implicitly_wait(2)

connection = sqlite3.connect('vendelux(sqlite3).db')
cursor = connection.cursor()

# Create the table (if it doesn't exist)
cursor.execute("""CREATE TABLE IF NOT EXISTS events (
    page_number INTEGER,
    Event TEXT,
    Date TEXT,
    Location TEXT,
    Price TEXT
)""")

for i in range(1, 11):
    url = 'https://vendelux.com/app/events/search?page=' + str(i)
    browser.get(url)

    names = browser.find_elements(By.CSS_SELECTOR, 'h6.MuiTypography-root')
    dates = browser.find_elements(By.CSS_SELECTOR, 'span.MuiTypography-root')
    locations = browser.find_elements(By.CSS_SELECTOR, '.MuiStack-root :nth-child(1) p')
    prices = browser.find_elements(By.CSS_SELECTOR, '.MuiStack-root :nth-child(3) p')

    for name, date, location, price in zip(names, dates, locations, prices):
        print(f"scraped from page {i} - Event: {name.text.strip()}")
        print(f"scraped from page {i} - date: {date.text.strip()}")
        print(f"scraped from page {i} - location: {location.text.strip()}")
        print(f"scraped from page {i} - price: {price.text.strip()}")
        event_info = (f"Page {i}", name.text.strip(), date.text.strip(), location.text.strip(), price.text.strip())
        cursor.execute("INSERT INTO events (page_number, Event, Date, Location, Price) VALUES (?, ?, ?, ?, ?)", event_info)

print("Finished scraping!")

# Commit changes and close connections
connection.commit()
browser.quit()
connection.close()
