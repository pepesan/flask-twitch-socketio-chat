import os
import json
import uuid
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Carga las variables de entorno desde .env
load_dotenv()

# Credenciales de servicio
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Crear conexión a la API de YouTube
youtube = build('youtube', 'v3', credentials=creds)

# Obtener los últimos videos publicados en un canal
channel_id = os.environ['YOUTUBE_CHANNEL_ID']  # Reemplazar con el ID del canal que te interesa

youtube.search()

search_response = youtube.search().list(
        part='id,snippet',
        channelId=channel_id,
        type='video',
        order='date',
        maxResults=10
    ).execute()

# Imprimir los títulos de los videos obtenidos
for search_result in search_response.get('items', []):
    title = search_result['snippet']['title']
    publishedAt = search_result['snippet']['publishedAt']
    # print(search_result['snippet'])
    print(f'Título: {title}')
    print(f'Fecha Publicación: {publishedAt}')

"""
id_suscripcion = str(uuid.uuid4())
try:
    suscripcion = youtube.subscriptions().insert(
        body={
            'snippet': {
                'resourceId': {
                    'kind': 'youtube#channel',
                    'channelId': channel_id
                }
            },
            'id': id_suscripcion,
            'type': 'web_hook',
            'address': 'https://tu-endpoint.com/notificar'
        }
    ).execute()
except HttpError as e:
    print('Se produjo un error al crear la suscripción: %s' % e)

"""