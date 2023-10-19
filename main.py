import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


FORMS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeHo7VWNXycmOv8pjMDxC9nWqjf8diGVkpzdGSdyVl-nHirAA/viewform?" \
            "usp=sf_link"
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22" \
             "usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.69219435644531%2C%22east%22%3A-122" \
             ".17446364355469%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22isMap" \
             "Visible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22" \
             "value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%" \
             "22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22" \
             "value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C" \
             "%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%" \
             "22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/106.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(ZILLOW_URL, headers=headers)
housing_page = response.text
soup = BeautifulSoup(housing_page, "html.parser")


# ----------------------------------------------- Create Link List ----------------------------------------------------

link_elements = soup.find_all(class_="StyledPropertyCardDataArea-c11n-8-70-0__sc-yipmu-0 dYZVUW property-card-link")
links_list = []
for link in link_elements:
    href = link["href"]
    if "http" not in href:
        links_list.append(f"https://www.zillow.com{href}")
    else:
        links_list.append(href)
print(links_list)

# --------------------------------------------- Create Address List ---------------------------------------------------

address_elements = soup.find_all(name="address")
address_list = [address.getText().split(" | ")[-1] for address in address_elements]
print(address_list)

# -------------------------------------------- Create Price List ------------------------------------------------------

price_elements = soup.find_all(class_="StyledPropertyCardDataArea-c11n-8-70-0__sc-yipmu-0 jSVWjf")
price_list = [price.get_text().split("+")[0] for price in price_elements if "$" in price.text]
print(price_list)

# ------------------------------------------- Create a google form ----------------------------------------------------

chrome_driver_path = r"C:\Users\Dewald\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

for i in range(len(links_list)):
    driver.get(FORMS_URL)

    time.sleep(2)
    address = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div'
                                                    '[1]/div/div[1]/input')
    price = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div'
                                                  '[1]/div/div[1]/input')
    link = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]'
                                                 '/div/div[1]/input')
    submit_button = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/'
                                                          'span')

    address.send_keys(address_list[i])
    price.send_keys(price_list[i])
    link.send_keys(links_list[i])
    submit_button.click()




