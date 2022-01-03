import requests
from bs4 import BeautifulSoup
import json
import os

def collectCatalogPageData(url, headers):
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    page_items_list = soup.find("div", class_="item-list").findAll("div", class_="item-list-item")

    page_data = []
    for page_item in page_items_list:
        page_item_image = "https://q-parser.ru" + page_item.find("img").get("src")
        page_item_title = page_item.find("a", class_="title").text.strip()
        page_item_link = page_item.find("a", class_="meta-text").get("href")
        page_item_country = page_item.find("div", class_="meta-text").text.strip()
        page_item_description = page_item.find("div", class_="meta-label").text.strip()

        page_item_data = {
            "Image": page_item_image,
            "Title": page_item_title,
            "Link": page_item_link,
            "Country": page_item_country,
            "Meta": page_item_description
        }

        page_data.append(page_item_data)

    return page_data

def createJsonFile(page_data, index):
    if not os.path.isdir('data'): os.mkdir("./data")
    with open(f"./data/data_{index}.json", "w", encoding="utf-8") as file:
        file.seek(0)
        json.dump(page_data, file, indent=4, ensure_ascii=False)

def main():
    url = "https://q-parser.ru/catalog"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36"
    }
    pages_count = 266

    for i in range(1, pages_count + 1):
        current_url = url if i == 1 else url + f"?page={i}"

        page_data = collectCatalogPageData(current_url, headers)
        data.append(page_data)

        print(f"Ready {i}/{pages_count}")
        createJsonFile(page_data, i)

if __name__ == "__main__":
    try:
        data = []
        main()
    except Exception:
        print(f"There is some error. Try again")
    else:
        print("All data has been collected. Check ./data")