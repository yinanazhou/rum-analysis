from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

os.environ[
    "PYDEVD_WARN_EVALUATION_TIMEOUT"
] = "5000"  # Set the timeout value in milliseconds


def loadWebsite(browser, url):
    try:
        browser.get(url)
    except:
        browser.quit()
        time.sleep(5)
        browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )

        browser.maximize_window()
        browser.get(url)
    return browser


df = pd.read_csv("./data/preprocessed.csv")
df = df[["Company", "Name"]]
price_df = pd.DataFrame(
    columns=[
        "Request",
        "Company",
        "Name",
        "Full Name",
        "Type",
        "Size",
        "Country",
        "Price",
    ]
)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--deny-permission-prompts")

browser = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=chrome_options
)

browser.maximize_window()

for idx, row in df.iterrows():
    item = {}
    browser = loadWebsite(browser, "https://www.saq.com/en/")

    try:
        browser.find_element(By.ID, "didomi-notice-agree-button").click()
    except:
        pass

    key = re.sub(
        r"\b(?:years?|years?)\b", "", (f"{row['Company']} {row['Name']}").lower()
    )
    try:
        browser.find_element(By.ID, "search").send_keys(key + Keys.RETURN)
    except:
        browser = loadWebsite(browser, "https://www.saq.com/en/")
        browser.find_element(By.ID, "search").send_keys(key + Keys.RETURN)

    item["Request"] = f"{row['Company']} {row['Name']}"
    try:
        try:
            # If returns multiple results
            result = browser.find_element(
                By.CSS_SELECTOR, ".products.list.items.product-items"
            )
            result.find_element(By.CSS_SELECTOR, ":first-child").click()
        except:
            pass

        try:
            item["Full Name"] = browser.find_element(By.CLASS_NAME, "page-title").text
        except:
            pass

        try:
            item["Type"] = browser.find_element(
                By.CSS_SELECTOR, "div.product.attribute.identity > span"
            ).text
        except:
            pass

        try:
            item["Size"] = browser.find_element(
                By.CSS_SELECTOR, "div.product.attribute.format > span > strong"
            ).text
        except:
            pass

        try:
            item["Country"] = browser.find_element(
                By.CSS_SELECTOR, "div.product.attribute.country > span > strong"
            ).text
        except:
            pass

        try:
            item["Price"] = browser.find_element(
                By.CSS_SELECTOR, ".price-wrapper > span"
            ).text.split("$")[1]

            # Only add to dataset if found price and is rum
            if item["Type"] and "rum" in str(item["Type"]).lower():
                item["Company"] = row["Company"]
                item["Name"] = row["Name"]
                price_df = pd.concat(
                    [price_df, pd.DataFrame([item])], ignore_index=True
                )
                print(idx, (f"{row['Company']} {row['Name']}: "), item["Price"])
        except:
            print(idx, f"Cannot find price for: {row['Company']} {row['Name']}")
    except:
        browser.quit()
        price_df.to_csv(f"price_{idx}.csv", index=False)

    # time.sleep(5)


price_df.to_csv("./data/price.csv", index=False)

print("done!")
