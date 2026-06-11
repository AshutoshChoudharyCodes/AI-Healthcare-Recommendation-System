import requests
from bs4 import BeautifulSoup

def extract_text(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["header", "footer", "nav", "aside", "script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = " ".join(text.split())

    title = soup.title.string if soup.title else "No Title"

    return text, title
