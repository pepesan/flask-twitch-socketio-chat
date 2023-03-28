# Servidor de Python para cliente del chat de twitch

## Instalación de dependencias
pip install -r requirements.txt

## Configuración

* Configura una nueva cuenta en Twitch para el bot
* Genera una nueva nueva aplicación en [https://dev.twitch.tv/](https://dev.twitch.tv/)
* Vete a Aplicaciones
* Registra tu aplicación
* Mete el nombre de la aplicación (nombre del bot)
* Mete una URL por ejemplo [http://localhost:5000/return](http://localhost:5000/return)
* Elige la categoría ChatBot
* Añadela
* Genera un nuevo Secreto
* Guarda el client ID y el Client Secret
* vete al la web [https://twitchtokengenerator.com/](https://twitchtokengenerator.com/)
* mete el client id y el client token
* Elige los scopes que necesites: normalmente chat:read y chat:edit 

### Copia el fichero .env.example a .env
cp .env.example .env
### Meter los datos de conexión
Edita el fichero .env con los datos del bot:
- nombre del bot
- 

## Arranque del servidor
./run.sh