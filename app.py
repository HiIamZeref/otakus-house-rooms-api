from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

CORS(app, origins='*')

""" CONECTAR AO BANCO """
cluster = MongoClient("mongodb+srv://pedroluiz:tez15kmClQy3m1fi@cluster0.wtvlihm.mongodb.net/?retryWrites=true&w=majority")
db = cluster['test']
collections = db['rooms']



@app.route("/rooms/", methods= ["GET"])
def rooms():
    """ GET ALL """
    all_rooms = collections.find()

    """ BUILD JSON """
    response_list = []
    for room in all_rooms:
        response_list.append(
            {
            "_id": str(room['_id']),
            "id": room['id'],
            "name": room['name'],
            "owner": room['owner'],
            "image": room['image'],
            "description": room['description'],
            "price": room['price'] ,
            "rating": room['rating'],
            "date": room['date']
    })
        
    return jsonify(response_list)


@app.route("/rooms/description/<int:id>", methods= ["GET"])
def get_unique_room(id):
    """ GET ONE """
    room = collections.find_one({"id": id})
    room_json = {
        "_id": str(room['_id']),
        "id": room['id'],
        "name": room['name'],
        "owner": room['owner'],
        "image": room['image'],
        "description": room['description'],
        "price": room['price'] ,
        "rating": room['rating'],
        "date": room['date']
    }

    return jsonify(room_json)


@app.route("/admin/rooms/", methods= ["POST"])
def add_room():
    room_json = {
        "id": int(request.args.get('id')),
        "name": request.args.get('name'),
        "owner": request.args.get('owner'),
        "image": request.args.get('image'),
        "description": request.args.get('description'),
        "price": request.args.get('price'),
        "rating": float(request.args.get('rating')),
        "date": request.args.get('date'),
    }

    collections.insert_one(room_json)

    return "Inserido com sucesso."


@app.route("/admin/rooms/<int:id>", methods= ["PUT", "DELETE"])
def alter_rooms(id):
    if request.method == "PUT":
        query = { "id": id }
        newvalues = { "$set": request.args }

        collections.update_one( query, newvalues)

        return "Atualizado com sucesso."


    elif request.method == "DELETE":
        query = {
            "id": id
        }

        collections.delete_one(query)

        return "Excluído com sucesso."





if __name__ == '__main__':
    app.run(debug=True)
