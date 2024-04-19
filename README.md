# eBay Price Scraper

This Python project is designed to scrape eBay for item prices, calculate the median price of products, and identify potential profitable items based on certain criteria. It leverages `aiohttp` for asynchronous HTTP requests, `BeautifulSoup` for parsing HTML, and `tqdm` for progress bars. The application runs on a Flask server, making it easy to interact with through a web interface.

## Features 🌟

- Asynchronous web scraping
- Median price calculation
- Profitable item detection based on custom price thresholds
- User-friendly web interface

## Installation 🛠️

Before you can run the application, you need to install the necessary Python packages. You can do this by running the following commands in your terminal:

```bash
pip install aiohttp beautifulsoup4 Flask tqdm
```

## Usage 🚀

To start the application, navigate to the project directory and run the following command:

```bash
python -m flask run --host=0.0.0.0 --port=8000
```

Once the server is running, you can access the web interface by visiting `http://localhost:8000` in your web browser. You'll be greeted with a simple form where you can enter the details for the eBay item you want to search for.

### API Endpoints

- **GET /**: Displays the main form to submit your search.
- **POST /**: Submits the form and displays the scraping results including median prices and potential profitable items.

## Contributing 🤝

Contributions to this project are welcome! Here are some ways you can contribute:

- Submitting bug reports and feature requests
- Writing code for new features or bug fixes
- Improving documentation

Please feel free to fork the repository and submit pull requests.

## Support 📢

If you encounter any problems or have any questions, please file an issue on GitHub. Your feedback is greatly appreciated!

## Acknowledgments 👏

- Special thanks to the Python community for maintaining such robust libraries that make projects like this possible.
