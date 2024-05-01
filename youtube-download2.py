
import requests
from bs4 import BeautifulSoup

# URL del canal de YouTube que deseas descargar
channel_url = 'https://www.youtube.com/c/CursosdeDesarrollo'

# Realiza una solicitud GET a la página del canal
response = requests.get(channel_url)

# Analiza la página HTML con BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Encuentra los enlaces de los videos en la página del canal
video_links = []
for link in soup.find_all('a', {'href': True}):
    href = link['href']
    if '/watch?v=' in href:
        video_links.append(f'https://www.youtube.com{href}')

print(video_links)
# Ahora puedes descargar los videos de la lista video_links
# Utiliza una biblioteca como 'youtube-dl' para descargarlos
