from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

BD = [
    {
        "alias": "GRodriguez",
        "nombre": "Gonzalo",
        "contactos": [{"alias": "PCesar", "nombre": "Cesar"}, {"alias": "PEddison", "nombre": "Eddison"},  {"alias": "JMarcelo", "nombre": "Marcelo"}],
        "enviados": [],
        "recibidos": []
    },
    {
        "alias": "PCesar",
        "nombre": "Cesar",
        "contactos": [{"alias": "PEddison", "nombre": "Eddison"}],
        "enviados": [],
        "recibidos": []
    },
    {
        "alias": "PEddison",
        "nombre": "Eddison",
        "contactos": [{"alias": "GRodriguez", "nombre": "Gonzalo"}],
        "enviados": [],
        "recibidos": []
    },
     {
        "alias": "JMarcelo",
        "nombre": "Marcelo",
        "contactos": [{"alias": "PEddison", "nombre": "Eddison"}],
        "enviados": [],
        "recibidos": []
    }
]

def findUser(alias):
    for user in BD:
        if user["alias"] == alias:
            return user
    return None

@app.route('/mensajeria/contactos', methods=['GET'])
def GetContactos():
    alias = request.args.get('mialias')
    usuario = findUser(alias)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    contactos = usuario["contactos"]
    return jsonify({c["alias"]: c["nombre"] for c in contactos}), 200

@app.route('/mensajeria/contactos/<alias>', methods=['POST'])
def AddContacto(alias):
    data = request.get_json()
    contacto_alias = data.get("contacto")
    contacto_nombre = data.get("nombre")

    usuario = findUser(alias)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    contacto = findUser(contacto_alias)
    if not contacto:
        nuevo_usuario = {
            "alias": contacto_alias,
            "nombre": contacto_nombre,
            "contactos": [],
            "enviados": [],
            "recibidos": []
        }
        BD.append(nuevo_usuario)
        contacto = nuevo_usuario

    if any(c["alias"] == contacto_alias for c in usuario["contactos"]):
        return jsonify({"mensaje": "El contacto ya existe en la lista"}), 400

    usuario["contactos"].append({"alias": contacto_alias, "nombre": contacto["nombre"]})
    return jsonify({"mensaje": "Contacto agregado exitosamente"}), 201

@app.route('/mensajeria/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    usuario_alias = data.get("usuario")
    contacto_alias = data.get("contacto")
    mensaje_contenido = data.get("mensaje")

    usuario = findUser(usuario_alias)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not any(c["alias"] == contacto_alias for c in usuario["contactos"]):
        return jsonify({"error": "El contacto no está en la lista de contactos"}), 400

    contacto = findUser(contacto_alias)
    if not contacto:
        return jsonify({"error": "Contacto no encontrado"}), 404

    mensaje = {
        "remitente": usuario["alias"],
        "destinatario": contacto["alias"],
        "contenido": mensaje_contenido,
        "fechaEnvio": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }
    usuario["enviados"].append(mensaje)
    contacto["recibidos"].append(mensaje)

    return jsonify({"mensaje": "Mensaje enviado exitosamente"}), 200

@app.route('/mensajeria/recibidos', methods=['GET'])
def mensajes_recibidos():
    alias = request.args.get('mialias')
    usuario = findUser(alias)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    mensajes = usuario["recibidos"]
    return jsonify(mensajes), 200

if __name__ == '__main__':
    app.run(debug=True)