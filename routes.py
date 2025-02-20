from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from models import User, db
from sqlalchemy.exc import IntegrityError

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user is not None  # Allow authentication only if user exists

def register_routes(app):
    
    @app.route('/')
    def home():
        return "Welcome to the User Management API! \n Add /users to the URL to display all the users."
    
    @app.route('/users', methods=['POST'])
    @auth.login_required
    def add_user():
        data = request.json
        if not data or "username" not in data or "password" not in data:
            return jsonify({"error": "Missing username or password"}), 400

        try:
            new_user = User(username=data["username"], password=data["password"])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User added successfully!"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Username already exists"}), 409

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    @app.route('/users', methods=['GET'])
    @auth.login_required
    def get_users():
        try:
            users = User.query.all()
            return jsonify([{"id": user.id, "username": user.username} for user in users])
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    @app.route('/users/<int:id>', methods=['GET'])
    @auth.login_required
    def get_user(id):
        try:
            user = User.query.get(id)
            
            if user is None:  # FIX: Check if user exists before accessing attributes
                return jsonify({"error": "User not found"}), 404

            return jsonify({"id": user.id, "username": user.username})
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    @app.route('/users/<int:id>', methods=['PUT'])
    @auth.login_required
    def update_user(id):
        try:
            user = User.query.get(id)
            if user is None:  # FIX: Check if user exists before updating
                return jsonify({"error": "User not found"}), 404
            
            data = request.json
            if "username" in data:
                user.username = data["username"]
            if "password" in data:
                user.password = data["password"]
            
            db.session.commit()
            return jsonify({"message": "User updated successfully!"})
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Username already exists"}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    @app.route('/users/<int:id>', methods=['DELETE'])
    @auth.login_required
    def delete_user(id):
        try:
            user = User.query.get(id)
            if user is None:  # FIX: Check if user exists before deleting
                return jsonify({"error": "User not found"}), 404
            
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
