import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = "https://www.flipkart.com/search?q=laptops"

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'lxml')

# Extract the required information from the HTML tags
product_titles = []
product_prices = []

for title in soup.find_all('div', class_='_4rR01T'):
    product_titles.append(title.text)

for price in soup.find_all('div', class_='_30jeq3 _1_WHN1'):
    product_prices.append(price.text)

# Print the extracted information
print("Product Titles:", product_titles)
print("Product Prices:", product_prices)
