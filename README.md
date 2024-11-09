# LIST: LinkedIn Scrapping Tool

### Prerequisites

- Python 3.x
- Selenium WebDriver
- Firefox browser
- Required Python packages:
  - selenium

## Profile URL Extractor

How to run the script (sample command):

```bash
python3 createProfileList.py --searchPatternURL "https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=FACETED_SEARCH&page={pageNumber}&schoolFilter=%5B%2215093696%22%5D&sid=PI%2C" --startPage 1 --endPage 2
```

This script extracts LinkedIn profile URLs from search results pages based on a given search pattern URL and stores them in a txt file.

# PROFILE SKILL SCRAPER

How to run the script (sample command):

```bash
python3 scrapProfiles.py --txtfile "path/to/profile_urls.txt" --outputFolder "path/to/output/folder" --startIndex 0 --endIndex -1
```

This script scrapes the skill information from LinkedIn profiles based on a given txt file containing the profile URLs and stores the scraped data in JSON files within a specified output folder.

Note: The `startIndex` and `endIndex` parameters are used to specify the range of profile URLs to scrape from the provided txt file. Setting `startIndex` to 0 and `endIndex` to -1 will scrape all profiles in the file.
