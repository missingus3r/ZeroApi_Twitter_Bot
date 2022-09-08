# pip install selenium
# pip install webdriver-manager

#libraries
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta

# Init
currency = "Dolar USA" # Opciones: Real, Euro, Peso Argentino
email = "mail@gmail.com"
contrasenia = "contraseña"
telefono = "091111111"

# Configuracion Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

#driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

# INE
print("Obteniendo datos del INE...")
driver.get("https://www.ine.gub.uy/cotizacion-de-monedas")

cells = driver.find_elements(By.XPATH,"//td[@role='gridcell']")

dolar_data = []
index = 0
loop = False
for data in cells:
    if data.text == currency:
        index = 0
        loop = True    
    if loop and index < 4:
        if index == 1:
            fecha = data.text[0:10]
            dolar_data.append(fecha)
        else:
            dolar_data.append(data.text)
        index=index+1
    else:
        loop = False

fecha_actual = datetime.today()
#fecha_actual = fecha_actual - timedelta(days=4) # DESCOMENTAR Y AJUSTAR EL days=x PARA FORZAR LA COTIZACION DE x DIAS ANTERIORES AL ACTUAL
fecha_actual = str(fecha_actual.day).zfill(2)+"/"+str(fecha_actual.month).zfill(2)+"/"+str(fecha_actual.year)

try:
    dolar_data.index(fecha_actual)
except:
    print("Cotizacion no disponible. Finalizado.")
    exit()

compra_actual = dolar_data[2]
compra_anterior = dolar_data[6]
venta_actual = dolar_data[3] 
venta_anterior = dolar_data[7]
print("Valor compra anterior: "+ compra_anterior)
print("Valor compra actual: "+ compra_actual)

# calculamos la diferencia con el ultimo dia habil y vemos si subio o bajo
diff = float(compra_actual) - float(compra_anterior)
if diff < 0:
    direccion  = "Bajando"
    percentage = str(round(100-((float(compra_actual)*100)/float(compra_anterior)),2)) + " %"
elif diff == 0:
    direccion = "Manteniendose igual"
    percentage = ""
else:
    direccion = "Subiendo"
    percentage = str(round(100-((float(compra_anterior)*100)/float(compra_actual)),2)) + " %"
    
compra_actual = str(round(float(compra_actual),2))

#------------------------------- START OF TWEET FORMATTING ------------------------
tweet = """El valor del dólar a la fecha es de: 
"""+compra_actual+""" pesos uruguayos
"""+direccion+""" """+percentage+"""
Fuente: https://ine.gub.uy     
#bot #dolar #pesos #uruguay #cotizacion #BCU #brou""" 
#------------------------------- END OF TWEET FORMATTING --------------------------

# TWITTER
driver.get("https://twitter.com/i/flow/login")
print("Entrando a Twitter...")
sleep(10)

email = driver.find_element(By.XPATH,"//input[@name='text']")
email.send_keys(email)
email.send_keys(Keys.TAB+Keys.ENTER)
print("Email ingresado")
sleep(10)

try:
    email = driver.find_element(By.XPATH,"//input[@name='text']")
    email.send_keys(telefono)
    email.send_keys(Keys.TAB+Keys.ENTER)
    print("Telefono ingresado")
except:
    print("Ingreso de telefono no necesario")
finally:
    sleep(10)
    password = driver.find_element(By.XPATH,"//input[@name='password']")
    password.send_keys(contrasenia)
    password.send_keys(Keys.TAB+Keys.TAB+Keys.TAB+Keys.ENTER)
    print("Password ingresada")
    
sleep(10)
tweet_box = driver.find_element(By.XPATH,"//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
tweet_box.send_keys(tweet)
tweet_box.send_keys(Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.ENTER)
print("Tweet publicado")
sleep(5)

driver.close()
driver.quit()