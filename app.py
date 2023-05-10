from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

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
            "id": room['id'],
            "name": room['name'],
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
        "id": room['id'],
        "name": room['name'],
        "image": room['image'],
        "description": room['description'],
        "price": room['price'] ,
        "rating": room['rating'],
        "date": room['date']
    }

    return jsonify(room_json)



if __name__ == '__main__':
    app.run(debug=True)
