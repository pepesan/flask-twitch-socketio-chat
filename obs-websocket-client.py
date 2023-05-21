import sys
import obsws_python as obs
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde .env
load_dotenv()

print(os.environ['OBS_PORT'])

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
if n < 2:
    exit(1)

print(sys.argv[1])
print(sys.argv[2])

# load conn info from config.toml
cl = obs.ReqClient(
    host=os.environ['OBS_HOST'],
    port=os.environ['OBS_PORT'],
    password=os.environ['OBS_PASSWORD'])


def cambia_escena(escena):
    print(f"Cambiando escena {escena}")
    cl.set_current_program_scene(escena)
    print("\nEscena:", escena)


def graba(efecto):
    print(f"graba {efecto}")
    if efecto == "on":
        cl.start_record()
    if efecto == "off":
        cl.stop_record()


def emite(efecto):
    print(f"emite {efecto}")
    if efecto == "on":
        cl.start_stream()
    if efecto == "off":
        cl.stop_stream()


def mute(fuente, efecto):
    print(f"mute {fuente} {efecto}")
    if efecto == "on":
        cl.set_input_mute(fuente, False)
    if efecto == "off":
        cl.set_input_mute(fuente, True)


#Pillar el listado de inputs
#resp = cl.get_input_list()
#print(resp.inputs)
#for input in resp.inputs:
#   print(input)

print("seleccionado comando")

if sys.argv[1] == "scene":
    print(sys.argv)
    cambia_escena(sys.argv[2])

if sys.argv[1] == "record":
    print(sys.argv)
    graba(sys.argv[2])

if sys.argv[1] == "emit":
    print(sys.argv)
    emite(sys.argv[2])

if sys.argv[1] == "mute":
    if n < 3:
        print("falta por definir la acción")
        exit(1)
    mute(sys.argv[2], sys.argv[3])
# GetVersion
# resp = cl.get_version()
# print(resp)
# Get Scenes
# resp = cl.get_scene_list()
# print(resp.scenes)
# for escena in resp.scenes:
#    print(escena)


# SetCurrentProgramScene
# cl.set_current_program_scene('Empezamos en breve')
# cl.set_current_program_scene('nuevo full david')
# cl.set_current_program_scene('nuevo full escritorio  y camara')
# cl.set_current_program_scene('Charlando con chat y alertas')
# cl.set_current_program_scene('Enseguida Volvemos')

# cambia_escena(sys.argv[2])



