import requests

response = requests.get('https://www.platzi.com') #devuelve un objeto response, es decir un objeto con la respuesta de un servidor html

print(dir(response)) # devuelve todos los métodos que se pueden usar

print(response.status_code) # devuelve el estado de la petición

print(response.headers) # Diccionario con información del sitio

print(response.headers['Date']) # Información específica

print(response.text) # Texto del html de la página