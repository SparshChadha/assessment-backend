# Assessment Backend - Time.com News Scraper API

A FastAPI-based web scraper that extracts the latest news stories from Time.com and provides them through a RESTful API endpoint.

## 📋 Overview

This project scrapes news articles from Time.com by parsing H3 elements containing story links and titles. It extracts up to 6 recent stories and serves them through a FastAPI web service.

## 🚀 Features

- Web Scraping: Fetches and parses HTML content from Time.com
- Story Extraction: Extracts news story titles and links from H3 elements
- RESTful API: Provides a clean JSON API endpoint
- Error Handling: Comprehensive error handling with appropriate HTTP status codes
- Data Persistence: Saves scraped data to local files for caching

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd assessment-backend-main
```

2. Install dependencies:
```bash
pip install fastapi uvicorn
```

3. Run the application:
```bash
uvicorn backend:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### GET `/getTimeStories`

Retrieves the latest news stories from Time.com.

Parameters:
- `fetch` (boolean, optional): Whether to fetch fresh data from Time.com. Default: `true`

Response:

Success (200):
```json
[
  {
    "title": "Story Title",
    "link": "https://time.com/article-url/"
  },
  ...
]
```

Error (502):
```json
{
  "error": "extracted_less_than_6",
  "extracted": 3,
  "stories": [...]
}
```

Error (500):
```json
{
  "detail": "Error message"
}
```

📁 Project Structure

```
assessment-backend-main/
├── backend.py          # FastAPI application and API endpoints
├── building_data.py    # Core scraping logic and data processing
├── stories.json        # Cached scraped stories (generated)
├── site.txt           # Cached HTML content from Time.com (generated)
└── README.md          # Project documentation
```

## 🔧 Core Components

`backend.py`
- FastAPI application setup
- `/getTimeStories` endpoint implementation
- Error handling and response formatting

`building_data.py`
- `getData()`: Downloads HTML content from Time.com
- `extract_h3_content()`: Parses HTML to find H3 elements
- `build_final_list()`: Extracts story titles and links
- `strip_tags()`: Removes HTML tags from text
- `extract_href()`: Extracts URLs from anchor tags
- `save_json()`: Saves data to JSON file

## 🎯 Usage Examples

Basic API Call
```bash
curl http://localhost:8000/getTimeStories
```

Skip Fresh Data Fetch
```bash
curl "http://localhost:8000/getTimeStories?fetch=false"
```

Using Python Requests
```python
import requests

response = requests.get("http://localhost:8000/getTimeStories")
stories = response.json()

for story in stories:
    print(f"Title: {story['title']}")
    print(f"Link: {story['link']}")
    print("---")
```

## 🔍 How It Works

1. Data Fetching: The application downloads the Time.com homepage HTML
2. HTML Parsing: Searches for `<h3>` elements containing story information
3. Link Extraction: Parses anchor tags within H3 elements to extract URLs and titles
4. Data Cleaning: Removes HTML tags and formats the extracted text
5. Response Formation: Returns a JSON array of story objects with title and link

## ⚠️ Error Handling

- HTTP 500: Server errors (network issues, parsing failures)
- HTTP 502: When fewer than 6 stories are extracted
- HTTP 200: Successful extraction of 6 or more stories

## 🧪 Running Standalone

You can also run the scraper directly without the API:

```bash
python building_data.py
```

This will:
- Fetch the latest data from Time.com
- Save it to `site.txt`
- Extract stories and save them to `stories.json`
- Print the results to console

## 📝 Notes

- The scraper targets Time.com's current HTML structure and may need updates if the site structure changes
- Cached data is stored in `site.txt` and `stories.json`
- The application expects at least 6 stories to be extracted for a successful response
- All URLs are converted to absolute URLs for consistency
