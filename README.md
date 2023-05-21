# Servidor de Python para cliente del chat de twitch

## Instalación de dependencias
pip install -r requirements.txt
## app.py (TwitchIO)
### Configuración

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

## bot-twitchapi-chat.py (TwitchAPI library)
* Configura una nueva cuenta en Twitch para el bot
* Genera una nueva nueva aplicación en [https://dev.twitch.tv/](https://dev.twitch.tv/)
* Vete a Aplicaciones
* Registra tu aplicación
* Mete el nombre de la aplicación (nombre del bot)
* Mete una URL por ejemplo [http://localhost:17563](http://localhost:17563)
* Elige la categoría ChatBot
* Añadela
* Genera un nuevo Secreto
* Guarda el client ID y el Client Secret
* Modifica el TWITCH_CLIENT_ID y el TWITCH_CLIENT_SECRET

## Cliente de Youtube
Para poder acceder al API de Youtube es necesario seguir una serie de pasos:
- Inicia sesión en la Consola de Desarrolladores de Google utilizando tu cuenta de Google en el siguiente enlace: https://console.developers.google.com/
- Crea un nuevo proyecto haciendo clic en el botón "Seleccionar proyecto" en la parte superior de la pantalla y luego en el botón "Nuevo proyecto".
- Asigna un nombre al proyecto y haz clic en el botón "Crear".
- Selecciona el proyecto recién creado haciendo clic en el botón "Seleccionar proyecto" en la parte superior de la pantalla y luego en el nombre del proyecto.
- Activa la API de YouTube haciendo clic en el botón "Habilitar API y servicios" en la página principal del proyecto.
- Busca "YouTube Data API v3" y selecciónala.
- Haz clic en el botón "Habilitar" para habilitar la API de YouTube.
- Haz clic en el botón "Crear credenciales" en la página principal del proyecto.
- Selecciona "Service Account" en el menú desplegable.
- Mete los datos: nombre del servicio, service-id y la descripción
- Pulsa en continuar
- En la selección de Rol deberías elegir el que te otorgue los privilegios adecuados
- Por ejemplo Owner te da todos los permisos
- Lo ideal es que seas conservador y pidas sólo los roles que necesites
- Después vuelve a pulsar Continuar
- Lo último sería seleccionar accesos individuales
- Si has seleccionado los roles necesarios puedes obviar esta parte y pulsar en Done
- Volverás a la página de credenciales y verás que aparece en la parte de Service Accounts tu Servicio
- Entra a ese servicio
- Pulsa en la pestaña Keys y dale a Add Key -> Create New Key
- Selecciona JSON y pulsa en Create
- Se descargará un fichero json
- Coloca el fichero en la carpeta principal del proyecto y renombralo a credentials.json

## TTS
### Ubuntu Install
$ sudo apt-get install portaudio19-dev
$ sudo apt-get install espeak

## GUI
### Desarrollo con Qt Designer (ubuntu 22.04)
sudo apt install designer-qt6
ir al directorio : /usr/lib/x86_64-linux-gnu/qtchooser
crear el fichero: qt6.conf
Meter el contenido:
/usr/lib/qt6/bin
/usr/lib/x86_64-linux-gnu

modificar el .bashrc al final:
export  QT_SELECT=qt6
### Official Guide 
https://doc.qt.io/qtforpython-6/gettingstarted/index.html

## Arrancar el QT6 Designer
designer




