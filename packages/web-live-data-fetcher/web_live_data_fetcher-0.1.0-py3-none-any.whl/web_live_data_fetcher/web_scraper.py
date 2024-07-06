import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string if soup.title else "No Title"
    body = soup.body
    body_text = body.get_text(separator='\n', strip=True) if body else "No Body Content"
    return title, body_text
