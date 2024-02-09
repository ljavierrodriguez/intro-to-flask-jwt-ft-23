from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


api = Blueprint('api', __name__)

@api.route('/test')
def test():
    return jsonify({"msg": "Testing API Routes"}), 200

@api.route('/get-token')
def get_token():
    token = create_access_token(identity="1")
    return jsonify({"token": token})
    
@api.route('/register', methods=['POST'])
def register():
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    userFound = User.query.filter_by(username=username).first()
    
    if userFound: return jsonify({"msg": "Usuario ya existe!"}), 400
    
    user = User()
    user.username = username
    user.password = generate_password_hash(password) # 123456 => eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MT
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({ "success": "Por favor inicie sesion!"}), 200

@api.route('/login', methods=['POST'])
def login():
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    userFound = User.query.filter_by(username=username).first()
    if not userFound: 
        return jsonify({"msg": "username/password son incorrectos"}), 401
    
    if not check_password_hash(userFound.password, password): 
        return jsonify({"msg": "username/password son incorrectos"}), 401
    
    acces_token = create_access_token(identity=userFound.id)
    
    datos = {
        "access_token": acces_token,
        "user": userFound.serialize()
    }
    
    return jsonify(datos)
    

@api.route('/test-private')
@jwt_required() # esta instruccion nos indica que esta ruta require del token para poder acceder
def private():
    return jsonify({"msg": "Testing Private API Routes"}), 200