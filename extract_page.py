import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://quotes.toscrape.com/"


def parse_quote(quote_div):
    text = quote_div.find("span", class_="text").get_text(strip=True)
    author = quote_div.find("small", class_="author").get_text(strip=True)

    tag_elements = quote_div.find_all("a", class_="tag")
    tags = [tag.get_text(strip=True) for tag in tag_elements]

    relative_link = quote_div.find("a")["href"]
    author_link = urljoin(base_url, relative_link)

    return {
        "text": text,
        "author": author,
        "tags": ", ".join(tags),
        "author_link": author_link,
    }


response = requests.get(base_url, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

quote_divs = soup.find_all("div", class_="quote")

all_quotes = []
for quote_div in quote_divs:
    listing = parse_quote(quote_div)
    all_quotes.append(listing)

print("Quotes found:", len(all_quotes))
for listing in all_quotes:
    print(listing["author"], "|", listing["tags"])