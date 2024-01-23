import aiohttp
import asyncio
import random
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys

MAX_THREADS = 45  # Maximum number of threads for concurrent requests
MAX_RETRIES = 3  # Maximum number of retries for failed requests

# User-Agent headers with an updated version
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.170 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/13.0.782.215 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/11.0.696.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/9.0.597.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/5.0.375.126 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/4.0.302.121 Safari/537.36",
]


def get_random_user_agent():
    return random.choice(USER_AGENT_LIST)

async def fetch_page_async(url, headers, retries=MAX_RETRIES):
    for _ in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.text()
        except aiohttp.ClientError:
            pass
        # Exponential backoff: wait for 2, 4, 8 seconds between retries
        await asyncio.sleep(2 ** _)
    return None

async def get_ebay_prices_async(item_name, page_limit):
    url = f"https://www.ebay.com/sch/i.html?_nkw={item_name.replace(' ', '+')}"
    tasks = []

    headers = {"User-Agent": get_random_user_agent()}

    # Limit the number of concurrent requests
    semaphore = asyncio.Semaphore(MAX_THREADS)

    async with aiohttp.ClientSession() as session:
        for page in range(1, page_limit + 1):
            url_with_page = f"{url}&_pgn={page}"
            tasks.append(fetch_page_async(url_with_page, headers))

        ebay_prices = []
        with tqdm(total=page_limit, desc="Fetching prices", unit="page") as pbar:
            for task in asyncio.as_completed(tasks):
                async with semaphore:
                    response = await task
                    if response:
                        soup = BeautifulSoup(response, "html.parser")
                        price_elements = soup.find_all("span", {"class": "s-item__price"})
                        for element in price_elements:
                            price = element.get_text()
                            try:
                                price_value = float(price.replace('$', '').replace(',', ''))
                                ebay_prices.append(price_value)
                            except ValueError:
                                pass
                pbar.update(1)

    return ebay_prices

async def calculate_median_price_async(prices):
    if not prices:
        return None
    sorted_prices = sorted(prices)
    middle_index = len(sorted_prices) // 2
    median_price = sorted_prices[middle_index] if len(sorted_prices) % 2 == 1 else (sorted_prices[middle_index - 1] + sorted_prices[middle_index]) / 2
    return median_price


async def find_potential_profitable_items_async(item_name, average_price, price_range_percentage, keywords):
    url = f"https://www.ebay.com/sch/i.html?_nkw={item_name.replace(' ', '+')}"
    headers = {"User-Agent": get_random_user_agent()}

    potential_items = []

    page = 1
    while True:
        url_with_page = f"{url}&_pgn={page}"
        response = await fetch_page_async(url_with_page, headers)
        if not response:
            #print(f"Failed to fetch data for page {page}. Skipping...")
            continue

        soup = BeautifulSoup(response, "html.parser")
        items = soup.select("li.s-item")
        for item in items:
            price_element = item.select_one("span.s-item__price")
            title_element = item.select_one("div.s-item__title")
            if price_element and title_element:
                try:
                    price_value = float(price_element.get_text().replace('$', '').replace(',', ''))
                    title = title_element.get_text().strip()

                    # Check if all keywords are present in the title
                    if all(keyword in title.lower() for keyword in keywords):
                        price_range_low = average_price * (100 - price_range_percentage) / 100
                        if price_value <= price_range_low:
                            link_element = item.select_one("a.s-item__link")
                            if link_element:
                                item_link = link_element.get("href")
                                condition_element = item.select_one("span.SECONDARY_INFO")
                                item_condition = condition_element.get_text().strip() if condition_element else "N/A"
                                seller_rating_element = item.select_one("span.s-item__seller-info-text")
                                seller_rating = seller_rating_element.get_text().strip() if seller_rating_element else "N/A"
                                shipping_element = item.select_one("span.s-item__shipping")
                                shipping_info = shipping_element.get_text().strip() if shipping_element else "N/A"

                                potential_items.append({
                                    "price": price_value,
                                    "link": item_link,
                                    "title": title,
                                    "condition": item_condition,
                                    "seller_rating": seller_rating,
                                    "shipping_info": shipping_info
                                })
                except ValueError:
                    pass

        next_page_link = soup.select_one("a.pagination__next")
        if not next_page_link:
            break

        page += 1

    potential_items.sort(key=lambda x: x["price"], reverse=True)  # Sort by price (most expensive to least expensive)

    with tqdm(total=len(potential_items), desc="Finding profitable items", unit="item") as pbar:
        for item in potential_items:
            await asyncio.sleep(0.01)  # Simulate processing time
            pbar.update(1)

    return potential_items

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        item_name = request.form["item_name"]
        page_limit = int(request.form["page_limit"])
        price_range_percentage = float(request.form["price_range_percentage"])

        # Retrieve keywords from the form
        keywords = request.form["keywords"].split(",") if request.form["keywords"] else []

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ebay_prices = loop.run_until_complete(get_ebay_prices_async(item_name, page_limit))
        average_price = loop.run_until_complete(calculate_median_price_async(ebay_prices))
        potential_profitable_items = loop.run_until_complete(
            find_potential_profitable_items_async(item_name, average_price, price_range_percentage, keywords)
        )

        return render_template(
            "result.html",
            item_name=item_name,
            page_limit=page_limit,
            price_range_percentage=price_range_percentage,
            average_price=average_price,
            potential_profitable_items=potential_profitable_items,
        )

    return render_template("index.html")


if __name__ == "__main__":
    host = "0.0.0.0"  # Listen on all available network interfaces
    port = 8000      # Choose the desired port

    print("Starting Flask app...")
    print(f"Access the app using: http://{host}:{port}/")
    app.run(host=host, port=port, debug=True)