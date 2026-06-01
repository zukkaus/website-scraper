import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import sys


def scrape_website(url: str) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    # --- Images ---
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        images.append({
            "src": urljoin(base_url, src),
            "alt": img.get("alt", ""),
            "title": img.get("title", ""),
        })

    # --- Links ---
    links = []
    seen_hrefs = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        if href in seen_hrefs:
            continue
        seen_hrefs.add(href)
        links.append({
            "text": a.get_text(strip=True),
            "href": href,
        })

    # --- Navigation menu items ---
    nav_items = []
    seen_nav = set()

    nav_selectors = [
        "nav",
        "[role='navigation']",
        ".nav", ".navbar", ".navigation", ".menu",
        "#nav", "#navbar", "#navigation", "#menu",
        "header ul", ".header ul", "#header ul",
    ]

    nav_containers = []
    for selector in nav_selectors:
        nav_containers.extend(soup.select(selector))

    # Deduplicate containers by identity
    seen_ids = set()
    unique_navs = []
    for el in nav_containers:
        eid = id(el)
        if eid not in seen_ids:
            seen_ids.add(eid)
            unique_navs.append(el)

    for nav in unique_navs:
        for a in nav.find_all("a", href=True):
            href = urljoin(base_url, a["href"])
            text = a.get_text(strip=True)
            key = (text, href)
            if key in seen_nav or not text:
                continue
            seen_nav.add(key)

            # Check for sub-menu siblings
            parent_li = a.find_parent("li")
            children = []
            if parent_li:
                sub_ul = parent_li.find("ul")
                if sub_ul:
                    for sub_a in sub_ul.find_all("a", href=True):
                        sub_href = urljoin(base_url, sub_a["href"])
                        sub_text = sub_a.get_text(strip=True)
                        if sub_text:
                            children.append({"text": sub_text, "href": sub_href})

            nav_items.append({"text": text, "href": href, "children": children})

    result = {
        "source_url": url,
        "images": images,
        "links": links,
        "navigation": nav_items,
        "summary": {
            "image_count": len(images),
            "link_count": len(links),
            "nav_item_count": len(nav_items),
        },
    }
    return result


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.washitavalleycac.com/"
    print(f"Scraping: {url}")

    data = scrape_website(url)

    output_file = "output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Done. Results saved to {output_file}")
    print(f"  Images found:          {data['summary']['image_count']}")
    print(f"  Links found:           {data['summary']['link_count']}")
    print(f"  Nav menu items found:  {data['summary']['nav_item_count']}")


if __name__ == "__main__":
    main()
