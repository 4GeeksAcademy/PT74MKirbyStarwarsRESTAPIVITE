"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Person, Planet, FavoritePlanets, FavoritePeople
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# Handle/serialize errors like a JSON object
@api.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@api.route('/')
def sitemap():
    return generate_sitemap(api)

@api.route('/people', methods=['GET'])
def get_people():
    response_body = Person.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@api.route('/planets', methods=['GET'])
def get_planets():
    response_body = Planet.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@api.route('/people/<int:person_id>', methods=['GET'])
def get_one_person(person_id):
    single_person = Person.query.get(person_id)
    
    if single_person is None:
        response = {
            "error": "These are not the droids you're looking for. Try again."
        }
        return jsonify(response), 404
    
    return jsonify(single_person.serialize()), 200

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    single_planet = Planet.query.get(planet_id)
    
    if single_planet is None:
        response = {
            "error": "That planet doesn't exist in this Universe. Try again. "
        }
        return jsonify(response), 404
    
    return jsonify(single_planet.serialize()), 200

#users and favorites

@api.route('/users', methods=['GET'])
def get_all_users():
    response_body = Users.query.all()
    response_body = list(map(lambda x: x.serialize(), response_body))
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    single_user = Users.query.get(user_id)
    
    if single_user is None:
        response = {
            "error": "Invalid user. Try again."
        }
        return jsonify(response), 404
    
    return jsonify(single_user.serialize()), 200

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_one_user_favorites(user_id):
    current_user = Users.query.get(user_id)
    favorite_planets = current_user.planet
    favorite_planets = [fav_planet.serialize() for fav_planet in favorite_planets]

    favorite_people = current_user.person
    favorite_people = [fav_char.serialize() for fav_char in favorite_people]

    user_favorites = favorite_people + favorite_planets

    return jsonify({ f"Current User '{current_user.username}' (id={current_user.id}) favorites": user_favorites }), 200

@api.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def add_one_person_to_favorites(user_id, person_id):
    char_exists = FavoritePeople.query.filter_by(person_id=person_id).filter_by(user_id=user_id).first()

    if not char_exists:
        favorite = FavoritePeople(user_id=user_id, person_id=person_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"status": f"Person '{favorite.person.name}' added to user '{favorite.user.username}' favorites."}), 200
    
    return jsonify({"status": f"Person '{Person.query.filter_by(id=person_id).first().name}' already in user '{Users.query.filter_by(id=user_id).first().username}' favorites."}), 200

@api.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_one_planet_to_favorites(user_id, planet_id):
    char_exists = FavoritePlanets.query.filter_by(planet_id=planet_id).filter_by(user_id=user_id).first()

    if not char_exists:
        favorite = FavoritePlanets(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"status": f"Planet '{favorite.planet.name}' added to user '{favorite.user.username}' favorites."}), 200
        
    return jsonify({"status": f"Planet '{Planet.query.filter_by(id=planet_id).first().name}' already in user '{Users.query.filter_by(id=user_id).first().username}' favorites."}), 200

@api.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_one_person_from_favorites(user_id, person_id):
    favorite = FavoritePeople.query.filter_by(person_id=person_id).filter_by(user_id=user_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"status": f"Person '{favorite.person.name}' deleted from user '{favorite.user.username}' favorites."}), 200

    return jsonify({"status": f"Nothing to delete: person '{Person.query.filter_by(id=person_id).first().name}' is not in user '{Users.query.filter_by(id=user_id).first().username}' favourites."}), 200

@api.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_one_planet_from_favorites(user_id, planet_id):
    favorite = FavoritePlanets.query.filter_by(planet_id=planet_id).filter_by(user_id=user_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"status": f"Planet '{favorite.planet.name}' deleted from user '{favorite.user.username}' favorites."}), 200
    
    return jsonify({"status": f"Nothing to delete: Planet '{Planet.query.filter_by(id=planet_id).first().name}' is not in user '{Users.query.filter_by(id=user_id).first().username}' favorites."}), 200


