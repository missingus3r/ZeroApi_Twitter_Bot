# ZeroApi_Twitter_Bot_V1.5
This is a bot for tweeting, made entirely in Python & without APIs!

Pueden ver el bot live en: 

	Dolar en Uruguay - Twitter : https://twitter.com/dolar_uruguay

Prerequisitos:

	Python 3.10
	
	Chrome
  
Librerias en python de:

	Selenium
	
	Webdriver-manager
   
Configuracion:

	Linea 15: currency = "Dolar USA"     -> Moenda, Opciones: Real, Euro, Peso Argentino
  
	Linea 16: email = "mail@gmail.com"   -> Email asociado a la cuenta de Twitter
  
	Linea 17: contrasenia = "contraseña" -> Contraseña de la cuenta de Twitter
	
	Línea 18: telefono = "091111111"     -> Número de movil asociado a la cuenta de Twitter
  
Para automatizar este bot, es necesario descargar el script y correrlo de forma automatica todos los dias despues de las 9, 
hora en la cual el INE publica las cotizaciones. Pueden correrlo en su propia PC (Linux, Windows o Mac) o en un server privado o remoto 24/7.

Pueden modificarlo a gusto para que el bot tome los datos de otra pagina, otras monedas, o los publique en otra red social.
Tambien pueden tomarlo como base para hacer su propio bot sin usar APIs!

Update 08/09/2022

	Mejoras:
		Posibilidad de publicar nuevas monedas: Real, Peso Argentino, Euro
		Funcionamiento en background! El script funciona sin abrir ventanas del Chrome
		Codigo mas limpio y mas compacto
		Menos librerias (quitada la librera de BeatifulSoup, ahora el bot usa solo selenium para el scrapping y el posteo en Twitter)
		Optimizado el tiempo de ejecucion, 40% mas rápido a la misma velocidad de internet

Mencionen si copian o modifican mi codigo!

Salu2!

missingus3r
