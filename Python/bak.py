# URL = "https://birds-europe.linnaeus.naturalis.nl/linnaeus_ng/app/views/introduction/topic.php?id=3432"
# page = requests.get(URL)
# print(page.text)



# soup = BeautifulSoup(page.content, "html.parser")
# # results = soup.find(id="content")

# print(soup.prettify())

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

DRIVER_PATH = './chromedriver'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

# url='https://birds-europe.linnaeus.naturalis.nl/linnaeus_ng/app/views/introduction/topic.php'
params ={'id':3432,'epi':207,'submit':''}

# # ?id=3432&epi=207

# response=requests.post(url, data=params)

driver.get("https://aetideidae.linnaeus.naturalis.nl/")
# print(driver.page_source)
h1 = driver.find_element(By.ID, 'lookupDialog')
# print(h1)
driver.quit()

from bs4 import BeautifulSoup

soup = BeautifulSoup(h1.text, "html5lib")
# print(soup.prettify)

# print(soup.prettify())

# results = soup.find(id="projects")



# https://aetideidae.linnaeus.naturalis.nl/linnaeus_ng/app/views/introduction/topic.php?id=3422&epi=193

# https://birds-europe.linnaeus.naturalis.nl/linnaeus_ng/app/views/introduction/topic.php?id=3422
# https://birds-europe.linnaeus.naturalis.nl/linnaeus_ng/app/views/introduction/topic.php?id=3423

