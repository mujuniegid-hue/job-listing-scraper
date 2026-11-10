import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://quotes.toscrape.com/"
DELAY_SECONDS = 1
MAX_PAGES = 20
OUTPUT_FILE = "quotes.csv"


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


def scrape_all_pages():
    all_quotes = []
    current_url = base_url
    page_number = 1

    while current_url and page_number <= MAX_PAGES:
        print("Scraping page", page_number, "->", current_url)

        response = requests.get(current_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for quote_div in soup.find_all("div", class_="quote"):
            all_quotes.append(parse_quote(quote_div))

        next_button = soup.find("li", class_="next")
        if next_button:
            next_href = next_button.find("a")["href"]
            current_url = urljoin(base_url, next_href)
        else:
            current_url = None

        page_number += 1
        time.sleep(DELAY_SECONDS)

    return all_quotes

def save_to_csv(rows, filename):
    fieldnames = ["text", "author", "tags", "author_link"]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

quotes = scrape_all_pages()
print("Total quotes scraped:", len(quotes))

quotes = scrape_all_pages()
print("Total quotes scraped:", len(quotes))

save_to_csv(quotes, OUTPUT_FILE)
print("Saved to", OUTPUT_FILE)