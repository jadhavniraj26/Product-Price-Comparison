import requests
import json

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import webbrowser
from bs4 import BeautifulSoup

from tkinter import *
import urllib
import math
from PIL import ImageTk, Image
from webdriver_manager.chrome import ChromeDriverManager

# Array for storing Daraz product after retrieving it from Daraz website

darazProductArr = []

# Array for storing Amazon product after retrieving it from Amazon website
amazonProductArr = []

# Array for storing Flipkart product after retrieving it from Amazon website
flipkartProductArr = []

# Array for storing Flipkart product after retrieving it from Amazon website
cromaProductArr =[]

root = Tk()
root.title("Product Price Comparison")
root.wm_state('zoomed')

# root.geometry("1000x1000")
search = StringVar()
state = StringVar()
state.set("Ready")

def USDtoINR(amount):
	url = f"https://api.apilayer.com/exchangerates_data/convert?to=INR&from=USD&amount={amount}"
	payload = {}
	headers = {
	  "apikey": "3s0PboHwgdGYDTykizxdJrH2f0osJut0"
	}
	response = requests.request("GET", url, headers=headers, data = payload)

	status_code = response.status_code
	result = response.text

	# converting string to dictionary
	r = json.loads(result)
	return f"Rs. {math.trunc(r['result'])}"


# Function to get products from Amazon
def getDetailsAmazon():
	# title = document.querySelectorAll(".s-title-instructions-style h2 a span")
	# price = .a-price .a-offscreen
	# link = .aok-relative span a
	# photo = .aok-relative span a div img
	amazonURL = f"https://www.amazon.com/s?k={search.get()}"
	# Entering options to not open the browser just get the data without opening the browser
	options = Options()
	options.add_argument('-headless')
	print("Search Started")
	state.set(f"Searching {search.get()} on Amazon")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	#driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
	driver.get(amazonURL)
	print("Search End")
	state.set(f"Searched Finished")

	print("Finding Elements")
	state.set(f"Finding Products....")

	# Finding Product title, price and photo
	title = driver.find_element(By.CSS_SELECTOR, ".s-title-instructions-style h2 a span")
	price = driver.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen")
	print(price)
	link = driver.find_element(By.CSS_SELECTOR, f".aok-relative span a").get_attribute("href")
	
	photo = driver.find_element(By.CSS_SELECTOR, f".aok-relative span a div img")
	print("Elements Found")	
	state.set(f"Products Found")

	print("Showing Elements on UI")	
	state.set(f"Showing Products")

	# Clearing all previous items from array
	amazonProductArr.clear()

	# Adding product to array
	amazonProductArr.append(link)

	amazonProductArr.append(title.text)
	inrPrice = USDtoINR(float(price.get_attribute("textContent")[1:]))
	amazonProductArr.append(inrPrice)

	amazonProductArr.append(photo.get_attribute("src"))

	print("Amazon Products Done")	
	state.set(f"Amazon Products Done")

	print(amazonProductArr)
	# Checking if no product found
	assert "No results found." not in driver.page_source
	driver.close()

	showAmazonProducts()

def getDetailsFlipkart():
	flipkartURL = f"https://www.flipkart.com/"
	# Entering options to not open the browser just get the data without opening the browser
	options = Options()
	options.add_argument('-headless')
	print("Search Started")
	state.set(f"Searching {search.get()} on Flipkart")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	driver.get(flipkartURL)
	print("Search End")
	state.set(f"Searched Finished")

	print("Finding Elements")
	state.set(f"Finding Products....")

	# locate the search bar element
	# enter the search query and press Enter
	driver.implicitly_wait(10)

	driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/button").click()
	input1 = search.get()
	driver.find_element(by=By.CLASS_NAME, value="_3704LK").send_keys(input1)
	driver.find_element(by=By.CLASS_NAME, value="L0Z3Pu").click()
	wait = WebDriverWait(driver, 10)
	#Click on the first search result
	# driver.find_element(by=By.CLASS_NAME, value="_2kHMtA").click()

	# Finding Product title, price and photo
	title = driver.find_element("css selector", '#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div.MIXNux > div._2QcLo- > div > div > img').get_attribute("alt")
	print(title)

	price = driver.find_element("css selector", "#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div._3pLy-c.row > div.col.col-5-12.nlI3QM > div._3tbKJL > div._25b18c > div._30jeq3._1_WHN1").text
	print(price)

	link = driver.find_element("css selector", "#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div.MIXNux > div._2QcLo- > div > div > img").get_attribute("baseURI")
	print(link)

	photo = driver.find_element("css selector", "#container > div > div._36fx1h._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div:nth-child(2) > div:nth-child(2) > div > div > div > a > div.MIXNux > div._2QcLo- > div > div > img").get_attribute("src")
	print(photo)
	print("Elements Found")
	state.set(f"Products Found")

	print("Showing Elements on UI")
	state.set(f"Showing Products")

	# Clearing all previous items from array
	flipkartProductArr.clear()

	# Adding product to array
	flipkartProductArr.append(link)

	flipkartProductArr.append(title)
	flipkartProductArr.append(price)

	flipkartProductArr.append(photo)

	print("Flipkart Products Done")
	state.set(f"Flipkart Products Done")

	print(flipkartProductArr)
	# Checking if no product found
	assert "No results found." not in driver.page_source
	driver.close()

	showflipkartProducts()


def getDetailsCroma():
	# title = document.querySelectorAll(".s-title-instructions-style h2 a span")
	# price = .a-price .a-offscreen
	# link = .aok-relative span a
	# photo = .aok-relative span a div img
	cromaURL = f"https://www.croma.com"

	#cromaURL = f"https://www.croma.com/search?q{search.get()}"
	# Entering options to not open the browser just get the data without opening the browser
	options = Options()
	options.add_argument('-headless')
	print("Search Started")

	state.set(f"Searching {search.get()} on Croma")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	# driver = webdriver.Chrome(options=options, executable_path=r'C:\WebBrowser\chromedriver_win32\chromedriver.exe')
	driver.get(cromaURL)
	print("Search End")
	state.set(f"Searched Finished")

	print("Finding Elements")
	state.set(f"Finding Products....")

	# locate the search bar element
	# enter the search query and press Enter
	#search_bar.clear()
	input=search.get()
	driver.find_element(By.ID, "searchV2").send_keys(input)
	driver.find_element(By.CSS_SELECTOR, ".input-wrap > div svg").click()
	wait = WebDriverWait(driver, 10)
	driver.implicitly_wait(10)


	#Finding Product title, price and photo
	title = driver.find_element("css selector", "#\32 67247 > div.product-info > div:nth-child(1) > h3" ).text
	print(title)
	price = driver.find_element("css selector", "#\32 67247 > div.product-info > div.price-rating-wrap.plp-price-margin.plp-prices > div.cp-price.main-product-price.pdp-cp-price > div > span").text
	print(price)
	link = driver.find_element("css selector", "#\32 61934 > #\32 67247 > div.product-info > div:nth-child(1) > h3").get_attribute("href")
	print(link)
	photo = driver.find_element("css selector" , "#\32 67247 > div.product-info > div:nth-child(1) > h3").get_attribute("src")
	print("Elements Found")
	state.set(f"Products Found")

	print("Showing Elements on UI")
	state.set(f"Showing Products")

	# Clearing all previous items from array
	cromaProductArr.clear()

	# Adding product to array
	cromaProductArr.append(link)

	cromaProductArr.append(title)

	#inrPrice = USDtoINR(float(price.get_attribute("textContent")[1:]))
	cromaProductArr.append(price)

	cromaProductArr.append(photo.get_attribute("src"))

	print("Croma Products Done")
	state.set(f"Croma Products Done")

	print(cromaProductArr)
	# Checking if no product found
	assert "No results found." not in driver.page_source
	driver.close()

	showCromaProducts()



# Function to get product of name entered by the user
def getDetailsDaraz():
	productClassName = "info--ifj7U"


	darazURL = f"https://www.daraz.pk/catalog/?q={search.get()}"
	# Entering options to not open the browser just get the data without opening the browser
	options = Options()
	options.add_argument('-headless')
	print("Search Started")
	state.set(f"Searching {search.get()} on DARAZ")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

	#driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
	driver.get(darazURL)
	print("Search End")
	state.set(f"Searching End")
	state.set(f"Finding Products on Daraz")

	print("Finding Elements")

	# Finding Product title, price and photo
	div = driver.find_element(By.CSS_SELECTOR, f".{productClassName} .title--wFj93 a")
	photo = driver.find_element(By.CSS_SELECTOR, ".img--VQr82 .mainPic--ehOdr a img").get_attribute("src")
	print(photo)
	price = driver.find_element(By.CSS_SELECTOR, f".{productClassName} .price--NVB62 span")
	

	link = div.get_attribute("href")
	title = div.text
	print("Elements Found")	
	state.set(f"Products found on DARAZ")

	print("Showing Daraz Products")	

	# Clearing all previous items from array
	darazProductArr.clear()

	# Adding prouduct to array
	darazProductArr.append(link)
	darazProductArr.append(title)
	darazProductArr.append(price.text)
	darazProductArr.append(photo)

	print("Elements Appear on UI")	
	state.set(f"Daraz Products Showed")


	# Checking if no product found
	assert "No results found." not in driver.page_source
	driver.close()

	showDarazProducts()


# Function to add spacing to text
def addSpacing(text):
	newText = ""
	i = 0
	text = text.split(" ")
	for val in text:
		if i == 10:
			newText += "\n "
			i = 0
		newText += f"{val} "
		i += 1
		
	return newText

def deleteFrame(frame):
	for item in frame.winfo_children():
		item.destroy()

	print("Items Deleted")


def showAmazonProducts():
	deleteFrame(amazonProductFrame)
	global amazonProductArr
	# Showing the Daraz product on UI
	darazTitle = Label(amazonProductFrame, text="AMAZON", font=("Calibri", 20, "bold"))
	darazTitle.pack()
	darazProductName = Label(amazonProductFrame, text=addSpacing(amazonProductArr[1]))  
	darazProductName.pack()

	darazPriceLabel = Label(amazonProductFrame, text=amazonProductArr[2])
	darazPriceLabel.pack()

	darazLinkBtn = Button(amazonProductFrame, text="Open in AMAZON", command=lambda: webbrowser.open(amazonProductArr[0]))
	darazLinkBtn.pack()


	# Showing Daraz product photo on UI
	raw_data = urllib.request.urlopen(amazonProductArr[3])
	u = raw_data.read()
	raw_data.close()

	photo = ImageTk.PhotoImage(data=u)
	label1 = Label(amazonProductFrame, image=photo, width=500, height=480)
	label1.image = photo
	label1.pack(side=RIGHT)

	print("Amazon DONE")

def showflipkartProducts():
		deleteFrame(flipkartProductFrame)
		global flipkartProductArr
		# Showing the Daraz product on UI
		darazTitle = Label(flipkartProductFrame, text="Flipkart", font=("Calibri", 20, "bold"))
		darazTitle.pack()
		darazProductName = Label(flipkartProductFrame, text=flipkartProductArr[1])
		darazProductName.pack()
		darazPriceLabel = Label(flipkartProductFrame, text=flipkartProductArr[2])
		darazPriceLabel.pack()

		darazLinkBtn = Button(flipkartProductFrame, text="Open in Flipkart", command=lambda: webbrowser.open(flipkartProductArr[0]))
		darazLinkBtn.pack()

		# Showing Daraz product photo on UI
		raw_data = urllib.request.urlopen(flipkartProductArr[3])
		u = raw_data.read()
		raw_data.close()

		photo = ImageTk.PhotoImage(data=u)
		label2 = Label(flipkartProductFrame, image=photo, width=500, height=500)
		label2.image = photo
		label2.pack(side=TOP)

		print("Flipkart DONE")


def showCromaProducts():
	deleteFrame(cromaProductFrame)
	global cromaProductArr
	# Showing the Daraz product on UI
	darazTitle = Label(cromaProductFrame, text="Croma", font=("Calibri", 20, "bold"))
	darazTitle.pack()
	darazProductName = Label(cromaProductFrame, text=addSpacing(cromaProductArr[1]))
	darazProductName.pack()

	darazPriceLabel = Label(cromaProductFrame, text=cromaProductArr[2])
	darazPriceLabel.pack()

	darazLinkBtn = Button(flipkartProductFrame, text="Open in Croma", command=lambda: webbrowser.open(flipkartProductArr[0]))
	darazLinkBtn.pack()


	# Showing Daraz product photo on UI
	raw_data = urllib.request.urlopen(cromaProductArr[3])
	u = raw_data.read()
	raw_data.close()

	photo = ImageTk.PhotoImage(data=u)
	label2 = Label(cromaProductFrame, image=photo, width=600, height=600)
	label2.image = photo
	label2.pack(side=BOTTOM)

	print("Croma DONE")



def showDarazProducts():
	deleteFrame(darazProductFrame)
	global darazProductArr
	# Showing the Daraz product on UI
	darazTitle = Label(darazProductFrame, text="DARAZ", font=("Calibri", 20, "bold"))
	darazTitle.pack()
	darazProductName = Label(darazProductFrame, text=addSpacing(darazProductArr[1]))  
	darazProductName.pack()

	darazPriceLabel = Label(darazProductFrame, text=darazProductArr[2])
	darazPriceLabel.pack()

	darazLinkBtn = Button(darazProductFrame, text="Open in DARAZ", command=lambda: webbrowser.open(darazProductArr[0]))
	darazLinkBtn.pack()


	# Showing Daraz product photo on UI
	raw_data = urllib.request.urlopen(darazProductArr[3])
	u = raw_data.read()
	raw_data.close()

	photo = ImageTk.PhotoImage(data=u)
	label1 = Label(darazProductFrame, image=photo, width=500, height=285)
	label1.image = photo
	label1.pack(side=RIGHT, pady=100)

	print("DONE")

# Main function that will run when user enter product name and click on SEARCH PRODUCT
def getResult():
	getDetailsDaraz()
	getDetailsAmazon()
	getDetailsFlipkart()
	#getDetailsCroma()
	state.set(f"Ready")




# Search Entry for entering product name on UI

root.configure(bg="#A4A4D3")
label = Label(root, text="Enter Search Result: ", bg="#A4A4D3" , anchor=CENTER , font=("Times New Roman", 25))
label.config(bg= "#A4A4D3", fg= "black")
label.place(relx = 0.4, rely = 0.3, anchor = CENTER)

label1 = Label(root, text="E-commerce Product Price Comparison",  font=("Times New Roman", 35, "bold"), anchor=CENTER)

label1.place(relx = 0.5, rely = 0.2, anchor = CENTER)

label1.config(bg= "#A4A4D3", fg= "black")
entry = Entry(root, textvariable=search, font=("Bold", 25))

entry.place(relx = 0.5, rely = 0.3, anchor =W)

button = Button(root, text="SEARCH PRODUCT", bg="#CDCDAA", command=getResult, activeforeground="red", activebackground="pink", pady=10, font=("Arial",15))
button.place(relx = 0.5, rely = 0.4, anchor =CENTER)


image = Image.open("C:\\Users\LENOVO\\Downloads\\Product-Price-Comparison-main\\OG-Banner-6.jpg")
resized_image = image.resize((600, 300))
photo = ImageTk.PhotoImage(resized_image)

# Create a label with the image
label5 = Label(root, image=photo)

# Position the label at (x, y) coordinates
label5.place(relx = 0.3, rely = 0.5)

# Product Frame for showing daraz and other websites product
productFrame = Frame(root, relief=SUNKEN)

# Daraz Frame where Daraz product will be shown
darazProductFrame = Frame(root)
darazProductFrame.pack(side=LEFT)

amazonProductFrame = Frame(root)
amazonProductFrame.pack(side=LEFT)

flipkartProductFrame = Frame(root)
flipkartProductFrame.pack(side=LEFT)

cromaProductFrame = Frame(root)
cromaProductFrame.pack(side=LEFT)


productFrame.pack(side=TOP, anchor=CENTER)


statusBar = Label(root, textvariable=state, relief=SUNKEN)
statusBar.pack(fill=X, side=BOTTOM)
#



root.mainloop()
