"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({"first_name": "John Jackson", "age": 33, "lucky_numbers": [7, 13, 22]})
jackson_family.add_member({"first_name":"Jane Jackson", "age": 35, "lucky_numbers": [10, 14, 3]})
jackson_family.add_member({"first_name":"Jimmy Jackson", "age": 5, "lucky_numbers": [1]})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }
    return jsonify(members), 200

# Endpoint para añadir un miembro de familia (POST)
@app.route('/member', methods=['POST'])
def add_family_member():
    data = request.json
    if not all(key in data for key in ["first_name", "id", "age", "lucky_numbers"]):
        return jsonify({"message": "Todos los campos son necesarios"}), 400
    jackson_family.add_member(data)
    return jsonify({"message": "Miembro de la familia añadido exitosamente"}), 200


# Endpoint para obtener un solo miembro de la familia (GET)
@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is not None:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Miembro de familia no encontrado"}), 400


# Endpoint para eliminar un miembro de la familia (DELETE)
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    eliminado = jackson_family.delete_member(member_id)
    if eliminado == True:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"Message": "Miembro de la familia no encontrado."}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
