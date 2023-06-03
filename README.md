# ValorDolarBot v2.0

This is the second version of a Python script that utilizes Selenium and BeautifulSoup to scrape the latest exchange rates of Dollar (USD) to Uruguayan Pesos (UYU) from the website https://www.brou.com.uy/cotizaciones. It calculates the percentage change from the previous value and then posts the information on Twitter.

## Features

- Scrape latest exchange rates of Dollar (USD) to Uruguayan Pesos (UYU) from the Banco Republica Oriental del Uruguay (BROU) website.
- Calculate percentage change from previous rates.
- Post the formatted information on Twitter.

## Prerequisites

- Python 3.x
- Selenium
- BeautifulSoup
- Google Chrome WebDriver

## Installation

1. Install Python 3.x from the official website: https://www.python.org/downloads/
2. Open a terminal or command prompt and install Selenium and BeautifulSoup using pip:

```
pip install selenium
pip install beautifulsoup4
```

3. Download the Google Chrome WebDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads. Extract the file and place it in the same directory as the script.

## Usage

1. Update the Twitter credentials (email, password and phone number) in the script:

```python
mail = "user@gmail.com"
contraseña = "password"
telefono = "111111111"
```

2. Run the script in the terminal or command prompt:

```
python ValorDolarBot_v2.0.py
```

The script will scrape the latest exchange rates, calculate the percentage change, and post the information on Twitter.

## Notes

- The script is designed to run in headless mode, meaning it does not display a browser window. However, if you prefer to see the browser window while the script is running, simply comment out or remove the following line:

```python
options.add_argument("--headless")
```

- The script currently deals only with the Dollar (USD) to Uruguayan Pesos (UYU) rates, but it can be easily adapted for other currencies as well.

## Contributions

Feel free to report bugs, contribute new features or improvements to the code. Contributions are more than welcome!

Salu2!

missingus3r
