from requests.auth import HTTPBasicAuth
import requests

resultado = requests.get('http://localhost:5000/login', auth=('juan', '123456'))
print(resultado.json())

resultado_autores = requests.get('http://localhost:5000/autores', headers={'x-access-token': resultado.json()[
    'token']})
print(resultado_autores.json())