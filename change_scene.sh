#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
fi

#conda info --envs >>  /home/pepesan/salida-streamdeck.txt
eval "$(conda shell.bash hook)"
conda activate streamdeck
echo "$1" >> /home/pepesan/salida-streamdeck.txt
echo "$2" >> /home/pepesan/salida-streamdeck.txt
echo "$3" >> /home/pepesan/salida-streamdeck.txt
python3 /home/pepesan/PycharmProjects/flask-twitch-socketio-chat/obs-websocket-client.py "$1" "$2" "$3"
