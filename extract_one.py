import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://quotes.toscrape.com/"

response = requests.get(base_url, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

first_quote = soup.find("div", class_="quote")

text = first_quote.find("span", class_="text").get_text(strip=True)
author = first_quote.find("small", class_="author").get_text(strip=True)

tag_elements = first_quote.find_all("a", class_="tag")
tags = [tag.get_text(strip=True) for tag in tag_elements]

relative_link = first_quote.find("a")["href"]
author_link = urljoin(base_url, relative_link)

listing = {
    "text": text,
    "author": author,
    "tags": ", ".join(tags),
    "author_link": author_link,
}

print(listing)