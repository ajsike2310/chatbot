import requests
from bs4 import BeautifulSoup
import os
import time

def parse_sitemap(sitemap_url):
    """
    Parse a sitemap XML URL or file, recursively extract all URLs.
    """
    urls = set()
    try:
        if sitemap_url.startswith("http"):
            response = requests.get(sitemap_url)
            response.raise_for_status()
            xml_content = response.text
        else:
            with open(sitemap_url, "r", encoding="utf-8") as f:
                xml_content = f.read()

        soup = BeautifulSoup(xml_content, "lxml-xml")

        # Check if it's a sitemap index (list of sitemap files)
        sitemap_tags = soup.find_all("sitemap")
        if sitemap_tags:
            for sitemap in sitemap_tags:
                loc = sitemap.find("loc").text.strip()
                urls.update(parse_sitemap(loc))  # recursive call
        else:
            # Normal sitemap - URLs
            url_tags = soup.find_all("url")
            for url in url_tags:
                loc = url.find("loc").text.strip()
                urls.add(loc)

    except Exception as e:
        print(f"Error parsing sitemap {sitemap_url}: {e}")

    return urls


def fetch_and_save_url(url, save_dir="output"):
    """
    Fetch the content of a URL and save it locally in save_dir.
    Filenames are created based on URL paths.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        # Create a safe filename from URL path
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_") + ".html"
        filepath = os.path.join(save_dir, filename)

        os.makedirs(save_dir, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Saved {url} -> {filepath}")

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")



if __name__ == "__main__":
    sitemap_path_or_url = "https://mbcet.ac.in/wp-sitemap.xml"  # or local file path

    print("Parsing sitemap to extract all URLs...")
    all_urls = parse_sitemap(sitemap_path_or_url)
    print(f"Found {len(all_urls)} URLs.")

    # Optional: limit number of pages to scrape for testing
    # all_urls = list(all_urls)[:10]

    for i, page_url in enumerate(all_urls, 1):
        print(f"[{i}/{len(all_urls)}] Fetching: {page_url}")
        fetch_and_save_url(page_url)
        time.sleep(1)  # be gentle on the server
