"""
Created by: Azhan Mohammed
Email: azhanmohammed1999@gmail.com
Description: Given a certain search pattern url, the script goes page wise and extracts the profile urls and stores them in a txt file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote
import time
import argparse
from tqdm import tqdm

def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract profile URLs from a search pattern URL.')
    parser.add_argument('--searchPatternURL', type=str, required=True, help='The search pattern URL to extract profiles from. The page number should be replaced by {pageNumber}.')
    parser.add_argument('--startPage', type=int, required=True, help='The start page number.')
    parser.add_argument('--endPage', type=int, required=True, help='The end page number.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    searchPatternURL = args.searchPatternURL
    startPage = args.startPage
    endPage = args.endPage

    # Initialize the WebDriver (make sure to have the appropriate driver installed, e.g., chromedriver)
    driver = webdriver.Firefox()
    driver.set_window_size(800, 600)

    # Open the provided URL
    linkedinUrl = "https://www.linkedin.com/uas/login"
    driver.get(linkedinUrl)

    while(True):
        feedUrl = "https://www.linkedin.com/feed/"
        if WebDriverWait(driver, 100).until(EC.url_to_be(feedUrl)):
            break

    print("Logged in successfully and changed to feed url")
    time.sleep(5)

    for pageNumber in tqdm(range(startPage, endPage+1)):
        searchURL = searchPatternURL.format(pageNumber=str(pageNumber))
        driver.get(searchURL)

        totalPageHeight = driver.execute_script("return document.documentElement.scrollHeight")
        currentPageHeight = 0

        while(True):
            if WebDriverWait(driver, 100).until(EC.url_to_be(searchURL)):
                break

        peopleLinks = []

        while(currentPageHeight<totalPageHeight):
            time.sleep(5)
            scrollDistance = int(totalPageHeight * (10 / 100))
            currentPageHeight = currentPageHeight + scrollDistance
            driver.execute_script(f"window.scrollTo(0, {currentPageHeight});")
            totalPageHeight = driver.execute_script("return document.documentElement.scrollHeight")
            try:
                peopleElements = driver.find_elements(By.XPATH, "//div[contains(@class, 't-roman t-sans')]//a[contains(@href, '?miniProfileUrn=')]")
                peopleUrl = [element.get_attribute("href") for element in peopleElements]
                peopleLinks.extend(peopleUrl)
            except:
                print("Element not found")
                time.sleep(5)
        peopleLinks = list(set(peopleLinks))
        peopleLinks = [link.split("?")[0]+"/" for link in peopleLinks]
        with open("outputList.txt", "a") as file:
            for link in peopleLinks:
                file.write(link + "\n")
    driver.quit()