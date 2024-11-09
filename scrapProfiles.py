"""
Created by: Azhan Mohammed
Email: azhanmohammed1999@gmail.com
Description: Given a txt file with profile urls, the script goes through each url and scrapes the profile skill information.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from urllib.parse import unquote
import json
from tqdm import tqdm
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract profile URLs from a search pattern URL.')
    parser.add_argument('--txtfile', type=str, required=True, help='The txt file containing the profile urls.')
    parser.add_argument('--outputFolder', type=str, required=True, help='The output folder to store the scraped data.')
    parser.add_argument('--startIndex', type=int, required=True, help='Start index of the profile urls to be scraped. Leave -1 to start from the beginning.')
    parser.add_argument('--endIndex', type=int, required=True, help='End index of the profile urls to be scraped. Leave -1 to scrape till the end.')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    txtfile = args.txtfile
    outputFolder = args.outputFolder
    startIndex = args.startIndex
    endIndex = args.endIndex
    with open(txtfile, 'r') as file:
        profileURLs = [line.strip() for line in file.readlines()]
    driver = webdriver.Firefox()
    driver.set_window_size(800, 600)

    # Open the provided URL
    linkedinUrl = "https://www.linkedin.com/uas/login"
    driver.get(linkedinUrl)
    if startIndex != -1:
        startIndex = startIndex
    else:
        startIndex = 0
    if endIndex != -1:
        endIndex = endIndex
    else:
        endIndex = len(profileURLs)
    for profileUrl in tqdm(profileURLs[startIndex:endIndex]):
        driver.get("https://www.linkedin.com/feed/")

        while(True):
            feedUrl = "https://www.linkedin.com/feed/"
            if WebDriverWait(driver, 100).until(EC.url_to_be(feedUrl)):
                break

        print("Logged in successfully and changed to feed url")
        time.sleep(5)
        driver.get(profileUrl)

        profilePicUrl = None
        try:
            image_element = driver.find_element(By.XPATH, "//img[contains(@class, 'pv-top-card-profile-picture__image--show')]")
            profilePicUrl = image_element.get_attribute("src")
        except Exception as e:
            print("An error occurred while finding the image:", str(e))

        name = None
        try:
            h1_element = driver.find_element(By.TAG_NAME, "h1")
            name = h1_element.text
        except Exception as e:
            print("An error occurred while finding the H1 tag:", str(e))

        totalPageHeight = driver.execute_script("return document.documentElement.scrollHeight")
        currentPageHeight = 0

        while(True):
            if WebDriverWait(driver, 100).until(EC.url_to_be(profileUrl)):
                break


        skillPageURL = None

        while(currentPageHeight<totalPageHeight):
            time.sleep(5)
            scrollDistance = int(totalPageHeight * (10 / 100))
            currentPageHeight = currentPageHeight + scrollDistance
            driver.execute_script(f"window.scrollTo(0, {currentPageHeight});")
            totalPageHeight = driver.execute_script("return document.documentElement.scrollHeight")
            try:
                element = driver.find_element(By.XPATH, "//a[contains(@href, '/details/skills?profileUrn')]")
                skillPageURL = element.get_attribute("href")
                driver.get(element.get_attribute("href"))
                break
            except:
                print("Element not found")
                time.sleep(5)

        time.sleep(20)

        currentPageHeight = 0

        skills = []

        while(currentPageHeight<totalPageHeight):
            try:
                time.sleep(5)
                scrollDistance = int(totalPageHeight * (10 / 100))
                currentPageHeight = currentPageHeight + scrollDistance
                driver.execute_script(f"window.scrollTo(0, {currentPageHeight});")
                skillElements = driver.find_elements(By.XPATH, "//a[@data-field='skill_page_skill_topic']")
                skill_links = [element.get_attribute("href") for element in skillElements]
                skillKeywords = [link.split("?keywords=")[1].split("&")[0] for link in skill_links]
                for skill in skillKeywords:
                    skills.append(skill)
                totalPageHeight = driver.execute_script("return document.documentElement.scrollHeight")
            except Exception as e:
                print("An error occurred while finding the div elements:", str(e))

        skills = set(skills)
        decodedSkills = [unquote(skill) for skill in skills]
        decodedSkills = [skill.replace("+", " ") for skill in decodedSkills]
        for skill in decodedSkills:
            while skill[-1] == " ":
                skill = skill[:-1]

        if name is None:
            name = ""
        if profilePicUrl is None:
            profilePicUrl = ""
        personData = {"profilePicUrl": profilePicUrl, "name": name, "skills": decodedSkills, "profileUrl": profileUrl}
        outputFileName = f'{outputFolder}/{name}.json'
        with open(outputFileName, 'w') as jsonFile:
            json.dump(personData, jsonFile, indent=4)