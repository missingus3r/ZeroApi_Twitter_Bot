# Instalar previamente las siguientes librerias:
# pip install selenium
# pip install webdriver-manager
# pip install bs4

#libraries
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

#------------------------------- START OF WEB SCRAPPING -----------------------------

url = 'https://www.ine.gub.uy/cotizacion-de-monedas' # El web scrapping del valor de las monedas se consigue desde la pagina del Insituto Nacional de Estadistica, es la mas estable y con valores de otras monedas
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# Limpiamos y formateamos la salida:
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out
# get text
text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

day = datetime.today().day # PARA CONSEGUIR LA COTIZACION DEL DIA DE ACTUAL
#day = 21 # PARA FORZAR LA COTIZACION DE UN DIA ESPECIFICO DENTRO DEL MES, PONER EL DIA
index = int(text.find("Dolar USA"+str(day).zfill(2)))

# si la cotizacion del dia no esta disponible todavia
if index == -1:
    print("Cotizacion no disponible. Finalizado.")
    exit()

# obtengo los chars y los convierto a un string, luego separo venta y compra
values = []
for i in range(index+9,index+37):
        values.append(text[i]) 
value = "".join(values)  #Ejemplo: Dolar USA30/08/2022 09:0039.450041.8500

#estos values[x:y] son substrings para, por posicion, leer solo los valores de compra y venta  
compra = value[16:21]
venta = value[23:29]

print("Valor compra actual: "+compra)

#valor compra del dia anterior valido
fecha_actual = value[0:10]
fecha_actual = datetime.strptime(fecha_actual,"%d/%m/%Y").date()

number_of_week = fecha_actual.weekday()

# si es lunes mirar la fecha del ultimo viernes
if number_of_week == 0:
    dia_anterior = fecha_actual - timedelta(days=3)
else:
    dia_anterior = fecha_actual - timedelta(days=1)
    
new_dia_anterior = dia_anterior.strftime('%d/%m/%Y')
index = int(text.find("Dolar USA"+str(new_dia_anterior).zfill(2)))

values = []
for i in range(index+9,index+37):
        values.append(text[i]) 
value_anterior = "".join(values) 
 
compra_anterior = value_anterior[16:21]
venta_anterior = value_anterior[23:29]

print("Valor compra anterior: "+compra_anterior)

#calculamos la diferencia con el ultimo dia valido y vemos si subio, bajo o se mantuvo
compra = float(compra)
compra_anterior = float(compra_anterior)
diff = compra - compra_anterior
direccion = "Subiendo"
percentage = 100-((compra_anterior*100)/compra)
percentage = str(round(percentage,2)) + " %"
if diff < 0:
    diff = compra_anterior-compra
    direccion  = "Bajando"
    percentage = 100-((compra*100)/compra_anterior)
    percentage = str(round(percentage,2)) + " %"
if diff == 0:
    direccion = "Manteniendose igual"
    percentage = ""

#------------------------------- END OF WEB SCRAPPING -----------------------------
#------------------------------- START OF TWEET FORMATTING ------------------------

tweet = """El valor del dólar a la fecha es de: 
"""+str(compra)+""" pesos uruguayos
"""+direccion+""" """+percentage+"""
Fuente: https://ine.gub.uy     
#bot #dolar #pesos #uruguay #cotizacion #BCU #brou""" 

#------------------------------- END OF TWEET FORMATTING --------------------------
#------------------------------------ START SELENIUM ------------------------------

#configuration
options = Options()
#options.add_argument("start-maximized")

#driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

#open webpage
driver.get("https://twitter.com/i/flow/login")
print("Pagina abierta")

sleep(15)

email = driver.find_element(By.XPATH,"//input[@name='text']")
email.send_keys("correo@gmail.com")
email.send_keys(Keys.TAB+Keys.ENTER)
print("Email ingresado")

sleep(15)

try: 
    # estas lineas son porque Twitter de forma aleatoria pregunta el numero de movil para evitar cuentas falsas, si lo pide, el bot lo ingresa, debe de estar previamente configurado en twitter
    email = driver.find_element(By.XPATH,"//input[@name='text']")
    email.send_keys("091111111")
    email.send_keys(Keys.TAB+Keys.ENTER)
    print("Telefono ingresado")
except:
    print("Ingreso de telefono no necesario")
finally:
    sleep(15)
    password = driver.find_element(By.XPATH,"//input[@name='password']")
    password.send_keys("CoNtRaSeÑaDeTwItTeR")
    password.send_keys(Keys.TAB+Keys.TAB+Keys.TAB+Keys.ENTER)
    print("Password ingresada")

sleep(15)

tweet_box = driver.find_element(By.XPATH,"//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
tweet_box.send_keys(tweet)
tweet_box.send_keys(Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.TAB+Keys.ENTER)
print("Tweet publicado")

sleep(5)

driver.close()
driver.quit()
#------------------------------------ END OF SELENIUM -----------------------------