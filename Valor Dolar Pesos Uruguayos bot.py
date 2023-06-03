# pip install selenium
# pip install webdriver-manager

import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# Set up headless Selenium driver
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

driver.get("https://www.brou.com.uy/cotizaciones")
html_content = driver.page_source

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
caja_full_div = soup.find("div", class_="caja full")

# Find the row containing "Dólar"
dolar_row = None
for row in caja_full_div.find_all("tr"):
    moneda = row.find("p", class_="moneda")
    if moneda and moneda.text.strip() == "Dólar":
        dolar_row = row
        break

# Extract the required values
if dolar_row:
    valor_elements = dolar_row.find_all("p", class_="valor")
    value_1 = float(valor_elements[0].text.strip().replace(',', '.'))
    value_2 = float(valor_elements[1].text.strip().replace(',', '.'))
else:
    print("Dólar values not found")

# Function to read previous values from the file
def read_previous_values(file_name):
    if not os.path.isfile(file_name):
        return None, None

    with open(file_name, "r") as f:
        contents = f.read().strip()
        values = contents.split(",")
        return float(values[0]), float(values[1])

# Function to write values to the file
def write_values_to_file(file_name, value_1, value_2):
    with open(file_name, "w") as f:
        f.write(f"{value_1},{value_2}")

file_name = "\history.txt"
previous_value_1, previous_value_2 = read_previous_values(file_name)

salida_venta=""
# Perform comparison and calculate percentage changes
if previous_value_1 and previous_value_2:
    
    print(f"Valor compra: {value_1}")
    print(f"Valor venta: {value_2}")
    
    change_1 = ((value_1 - previous_value_1) / previous_value_1) * 100
    change_2 = ((value_2 - previous_value_2) / previous_value_2) * 100

    if change_1 == 0:
        salida_compra="Manteniendose igual."
    else:
        salida_compra=f"{'Subiendo' if change_1 > 0 else 'Bajando'} {abs(change_1):.2f}%"

    if change_2 == 0:
        salida_venta="Manteniendose  igual."
    else:
        salida_venta=f"{'Subiendo' if change_2 > 0 else 'Bajando'} {abs(change_2):.2f}%"
        
# Init
mail = "mail@mail.com"
contrasenia = "abcd1234"
telefono = "+598091111111" # Just if twitter login telephone number verification is activated

venta_actual = str(value_2)+" pesos uruguayos. "+salida_venta
#------------------------------- START OF TWEET FORMATTING ------------------------
tweet = "El valor del dólar a la fecha es de: \n{venta_actual}\nFuente: https://www.brou.com.uy/cotizaciones\n#bot #dolar #pesos #uruguay #cotizacion #BCU #brou".format(venta_actual=venta_actual)
#------------------------------- END OF TWEET FORMATTING --------------------------
print("Tweet a publicar: "+tweet)

# TWITTER
driver.get("https://twitter.com/i/flow/login")
print("Entrando a Twitter...")

xpath = "//input[@name='text']"
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,xpath)))
email = driver.find_element(By.XPATH,xpath)
email.send_keys(mail+Keys.TAB+Keys.ENTER)
print("Email ingresado")

try:
    xpath = "//input[@name='text']"
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,xpath)))
    telefono = driver.find_element(By.XPATH,xpath)
    telefono.send_keys(telefono+Keys.TAB+Keys.ENTER)
    print("Telefono ingresado")
except:
    print("Ingreso de telefono no necesario")
    sleep(15)
finally:
    xpath = "//input[@name='password']"
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
    password = driver.find_element(By.XPATH,"//input[@name='password']")
    password.send_keys(contrasenia+Keys.TAB+Keys.TAB+Keys.TAB+Keys.ENTER)
    print("Password ingresada")
    
xpath = "//div[@class='notranslate public-DraftEditor-content']"
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,xpath)))
tweet_box = driver.find_element(By.XPATH,xpath)
tweet_box.send_keys(""+tweet+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.ENTER)
print("Tweet publicado")
sleep(10)

driver.close()
driver.quit()

# Update the local text file with the new values
write_values_to_file(file_name, value_1, value_2)
