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
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
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

    async with aiohttp.ClientSession() as session:
        for page in range(1, page_limit + 1):
            url_with_page = f"{url}&_pgn={page}"
            tasks.append(fetch_page_async(url_with_page, headers))

    ebay_prices = []
    with tqdm(total=page_limit, desc="Fetching prices", unit="page") as pbar:
        for task in asyncio.as_completed(tasks):
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

async def calculate_average_price_async(prices):
    if not prices:
        return None
    average_price = sum(prices) / len(prices)
    with tqdm(total=100, desc="Calculating average price", unit="%", ncols=100) as pbar:
        for i in range(100):
            pbar.update(1)
            await asyncio.sleep(0.01)  # Simulate calculation time
    return average_price

async def find_potential_profitable_items_async(item_name, average_price, price_range_percentage):
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
            if price_element:
                try:
                    price_value = float(price_element.get_text().replace('$', '').replace(',', ''))
                    price_range_low = average_price * (100 - price_range_percentage) / 100
                    if price_value <= price_range_low:
                        link_element = item.select_one("a.s-item__link")
                        if link_element:
                            item_link = link_element.get("href")
                            title_element = item.select_one("div.s-item__title")
                            item_title = title_element.get_text().strip() if title_element else "N/A"
                            condition_element = item.select_one("span.SECONDARY_INFO")
                            item_condition = condition_element.get_text().strip() if condition_element else "N/A"
                            seller_rating_element = item.select_one("span.s-item__seller-info-text")
                            seller_rating = seller_rating_element.get_text().strip() if seller_rating_element else "N/A"
                            shipping_element = item.select_one("span.s-item__shipping")
                            shipping_info = shipping_element.get_text().strip() if shipping_element else "N/A"

                            potential_items.append({
                                "price": price_value,
                                "link": item_link,
                                "title": item_title,
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

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ebay_prices = loop.run_until_complete(get_ebay_prices_async(item_name, page_limit))
        average_price = loop.run_until_complete(calculate_average_price_async(ebay_prices))
        potential_profitable_items = loop.run_until_complete(
            find_potential_profitable_items_async(item_name, average_price, price_range_percentage)
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
    app.run(host="0.0.0.0", port=8000, debug=True)