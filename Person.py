import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import unquote
import json

class PersonProfileScrapper:
    def __init__(self, driver, personprofileurl, extractionFields):
        self.driver = driver
        self.personName = None
        self.personprofileurl = personprofileurl
        self.personProfilePictureUrl = None
        self.personExperienceUrl = f"{personprofileurl}details/experience/"
        self.personExperience = None
        self.personSkillUrl = f"{personprofileurl}details/skills/"
        self.personSkill = None
        self.personDetails = None
        self.extractionFields = extractionFields

    def extractSkills(self):
        self.driver.get(self.personSkillUrl)
        while(True):
            if WebDriverWait(self.driver, 100).until(EC.url_to_be(self.personSkillUrl)):
                break
        currentPageHeight = 0
        skills = []
        totalPageHeight = self.driver.execute_script("return document.documentElement.scrollHeight")
        while(currentPageHeight<totalPageHeight):
            try:
                time.sleep(5)
                scrollDistance = int(totalPageHeight * (30 / 100))
                currentPageHeight = currentPageHeight + scrollDistance
                self.driver.execute_script(f"window.scrollTo(0, {currentPageHeight});")
                skillElements = self.driver.find_elements(By.XPATH, "//a[@data-field='skill_page_skill_topic']")
                skill_links = [element.get_attribute("href") for element in skillElements]
                skillKeywords = [link.split("?keywords=")[1].split("&")[0] for link in skill_links]
                for skill in skillKeywords:
                    skills.append(skill)
                totalPageHeight = self.driver.execute_script("return document.documentElement.scrollHeight")
            except Exception as e:
                print("An error occurred while finding the div elements:", str(e))
        skills = set(skills)
        decodedSkills = [unquote(skill) for skill in skills]
        decodedSkills = [skill.replace("+", " ") for skill in decodedSkills]
        for skill in decodedSkills:
            while skill[-1] == " ":
                skill = skill[:-1]
        self.personSkill = decodedSkills

    def extractBasics(self):
        self.driver.get(self.personprofileurl)
        time.sleep(10)
        try:
            imageElement = self.driver.find_element(By.XPATH, "//img[contains(@class, 'pv-top-card-profile-picture__image--show')]")
            self.personProfilePictureUrl = imageElement.get_attribute("src")
        except Exception as e:
            print("An error occurred while finding the image:", str(e))
        try:
            h1_element = self.driver.find_element(By.TAG_NAME, "h1")
            self.personName = h1_element.text
        except Exception as e:
            print("An error occurred while finding the H1 tag:", str(e))

    def extractExperience(self):
        self.driver.get(self.personExperienceUrl)
        while(True):
            if WebDriverWait(self.driver, 100).until(EC.url_to_be(self.personExperienceUrl)):
                break
        time.sleep(20)
        experienceData = None
        try:
            experienceElements = self.driver.find_elements(By.XPATH, "//div[@data-view-name='profile-component-entity']")
            experienceElement = experienceElements[0]
            imgElement = experienceElement.find_element(By.XPATH, ".//img[contains(@src, 'company-logo_100_100')]")
            companyLogoUrl = imgElement.get_attribute("src")
            try:
                companyNameElement = experienceElement.find_element(By.XPATH, ".//span[contains(@class, 't-14 t-normal')]")
                companyName = companyNameElement.find_element(By.XPATH, ".//span[@aria-hidden='true']").text
                subComponentsElement = experienceElement.find_element(By.XPATH, ".//div[contains(@class, 'display-flex full-width')]")
                positionElement = subComponentsElement.find_element(By.XPATH, ".//div[contains(@class, ' mr1 t-bold')]")
                positionNameElement = positionElement.find_element(By.XPATH, ".//span[@aria-hidden='true']")
                positionName = positionNameElement.text
                experienceData = {"companyLogoURL": companyLogoUrl, "companyName": companyName, "positionName": positionName}
            except:
                companyNameElement = experienceElement.find_element(By.XPATH, ".//div[contains(@class, 'hoverable-link-text t-bold')]")
                companyName = companyNameElement.find_element(By.XPATH, ".//span[@aria-hidden='true']").text
                subComponentsElement = experienceElement.find_element(By.XPATH, ".//div[contains(@class, 'pvs-entity__sub-components')]")
                positionElement = subComponentsElement.find_elements(By.XPATH, ".//div[contains(@class, 'hoverable-link-text t-bold')]")
                positionElement = positionElement[0]
                positionNameElement = positionElement.find_element(By.XPATH, ".//span[@aria-hidden='true']")
                positionName = positionNameElement.text
                experienceData = {"companyLogoURL": companyLogoUrl, "companyName": companyName, "positionName": positionName}
            self.personExperience = experienceData
        except Exception as e:
            print("An error occurred while finding the experience div elements:", str(e))

    def getAllDetails(self):
        self.extractBasics()
        if self.extractionFields["extractExperience"]:
            self.extractExperience()
        if self.extractionFields["extractSkills"]:
            self.extractSkills()
        self.personDetails = {
            "personName": self.personName,
            "personProfilePictureUrl": self.personProfilePictureUrl,
            "personExperience": self.personExperience,
            "personSkill": self.personSkill
        }
    
    def savePersonDetails(self):
        with open(f"./peopleData/{self.personName}.json", "w") as file:
            json.dump(self.personDetails, file)