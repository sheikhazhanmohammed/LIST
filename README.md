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