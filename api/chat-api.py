from flask import Flask, jsonify

app1 = Flask(__name__)
app2 = Flask(__name__)


# Definir una ruta y su método HTTP asociado
@app1.route('/api/chat', methods=['GET'])
def chat():
    # Lógica para procesar la solicitud
    datos = {
        'mensaje': 'Hola, mundo!',
        'autor': "cursosdedesarrollo"
    }

    # Devolver una respuesta en formato JSON
    return datos


@app2.route('/app2')
def app2_route():
    return 'Este es el servidor 2'


# Punto de entrada para la aplicación
if __name__ == '__main__':
    app1.run(debug=True, port=5000)
    app2.run(debug=True, port=5001)
