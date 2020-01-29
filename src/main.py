"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Tarea
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route("/todos/<username>", methods=["GET", "POST", "PUT", "DELETE"])
def handle_tarea(username):
    headers = {
        "Content-Type": "application/json"
    }
    requesting_user = User.query.filter_by(username=username).all()
    if request.method == "GET":
        print("hello i'm working!")
        if len(requesting_user) > 0:
            print("user exists")
            user_todo_list = Tarea.query.filter_by(user_username=username).all()
            response_body = []
            for tareas in user_todo_list:
                response_body.append(tareas.serialize())
            status_code = 200
        else:
            print("User doesn't exist")
            response_body={
                "status": "HTTP_404_NOT_FOUND. User does not exist"
            }
            status_code = 404
    elif request.method == "POST":
        print("creating user con sample task")

        if len(requesting_user) > 0:
            response_body = {
                "status": "HTTP_400_BAD_REQUEST. User cannot be created again..."
            }
            status_code = 400

        else:
            print("creating user with this username")
            new_user = User(username)
            db.session.add(new_user)
            sample_todo = Tarea("Toma agua", username)
            db.session.commit()
            response_body = {
                "status": "HTTP_200_OK. Ok"
            }
            status_code = 200
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
