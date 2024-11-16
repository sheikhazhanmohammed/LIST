"""
Created by: Azhan Mohammed
Email: azhanmohammed1999@gmail.com
Description: Given a txt file with profile urls, the script goes through each url and scrapes the profile skill information.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import argparse
from Person import PersonProfileScrapper
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract profile URLs from a search pattern URL.')
    parser.add_argument('--txtfile', type=str, required=True, help='The txt file containing the profile urls.')
    parser.add_argument('--startIndex', type=int, required=True, help='Start index of the profile urls to be scraped. Leave -1 to start from the beginning.')
    parser.add_argument('--endIndex', type=int, required=True, help='End index of the profile urls to be scraped. Leave -1 to scrape till the end.')
    parser.add_argument('--extractExperience', type=bool, default=True, required=False, help='End index of the profile urls to be scraped. Leave -1 to scrape till the end.')
    parser.add_argument('--extractSkill', type=bool, default=True, required=False, help='End index of the profile urls to be scraped. Leave -1 to scrape till the end.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    txtfile = args.txtfile
    startIndex = args.startIndex
    endIndex = args.endIndex
    extractExperience = args.extractExperience
    extractSkill = args.extractSkill
    os.makedirs("./peopleData", exist_ok=True)
    with open(txtfile, 'r') as file:
        profileURLs = [line.strip() for line in file.readlines()]
    driver = webdriver.Firefox()
    driver.set_window_size(800, 600)

    # Open the provided URL
    linkedinUrl = "https://www.linkedin.com/uas/login"
    driver.get(linkedinUrl)
    while(True):
        feedUrl = "https://www.linkedin.com/feed/"
        if WebDriverWait(driver, 100).until(EC.url_to_be(feedUrl)):
            break
    if startIndex != -1:
        startIndex = startIndex
    else:
        startIndex = 0
    if endIndex != -1:
        endIndex = endIndex
    else:
        endIndex = len(profileURLs)
    for profileUrl in tqdm(profileURLs[startIndex:endIndex]):
        person = PersonProfileScrapper(driver, profileUrl, {"extractExperience": extractExperience, "extractSkills": extractSkill})
        person.getAllDetails()
        person.savePersonDetails()