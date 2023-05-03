from selenium import webdriver

# Set up the webdriver
driver = webdriver.Chrome()

# Navigate to the webpage you want to scrape
url = "https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
driver.get(url)

# Find all the product names
#product_names = driver.find_elements_by_css_selector("div._4rR01T")

# Find all the product prices
#product_prices = driver.find_elements_by_css_selector("div._30jeq3._1_WHN1")
product = driver.find_element("css selector", '#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div.MIXNux > div._2QcLo- > div > div > img')


# Find all the product prices
product_prices = driver.find_element("css selector", "#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div._3pLy-c.row > div.col.col-5-12.nlI3QM > div._3tbKJL > div._25b18c > div._30jeq3._1_WHN1")

# Print the product names and prices
#for i in range(len(product)):
print("Product Name:", product.get_attribute("alt"))
print("Product Price:", product_prices.text)

# Close the webdriver
driver.quit()
