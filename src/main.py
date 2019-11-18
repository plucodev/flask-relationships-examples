"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Image
#from models import Person
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)




app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # if username != 'test' or password != 'test':
    #     return jsonify({"msg": "Bad username or password"}), 401
    usercheck = User.query.filter_by(username=username, password=password).first()
    if usercheck == None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=username), 'id':usercheck.id}
    return jsonify(ret), 200

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
@app.route('/users', methods=['GET'])
def handle_users():
    all_people = User.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

@app.route('/adduser', methods=['POST'])
def handle_user():
    body = request.get_json()

        # if body is None:
        #     raise APIException("You need to specify the request body as a json object", status_code=400)
        # if 'username' not in body:
        #     raise APIException('You need to specify the username', status_code=400)
        # if 'email' not in body:
        #     raise APIException('You need to specify the email', status_code=400)

    user1 = User(username=body['username'], email=body['email'], password=body['password'])
    db.session.add(user1)
    db.session.commit()
    return "ok", 200
@app.route('/addImage', methods=['POST'])
def handle_image():
    body = request.get_json()

        # if body is None:
        #     raise APIException("You need to specify the request body as a json object", status_code=400)
        # if 'username' not in body:
        #     raise APIException('You need to specify the username', status_code=400)
        # if 'email' not in body:
        #     raise APIException('You need to specify the email', status_code=400)

    image1 = Image(image_name=body['image_name'], user_id=body['user_id'])
    db.session.add(image1)
    db.session.commit()
    return "ok", 200


@app.route('/hello', methods=['POST', 'GET'])
@jwt_required
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
